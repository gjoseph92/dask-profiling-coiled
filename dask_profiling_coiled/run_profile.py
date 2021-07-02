import asyncio
import sys
import time

import coiled
import dask
import dask.dataframe
import distributed
import psutil

from scheduler_profilers import pyspy_on_scheduler

from .sizeof_graph import print_sizeof_serialized_graph


def main() -> float:
    df = dask.datasets.timeseries(
        start="2000-01-01",
        end="2000-06-30",  # 720 ~partitions
        partition_freq="1h",
        freq="60s",
    )
    df = df.persist()
    distributed.wait(df)
    print("DataFrame persisted")

    shuffled = df.shuffle("id", shuffle="tasks")

    print_sizeof_serialized_graph(shuffled)

    start = time.perf_counter()
    df2 = shuffled.persist()
    distributed.wait(df2)
    elapsed = time.perf_counter() - start
    return elapsed


if __name__ == "__main__":
    n_workers = 100
    cluster = coiled.Cluster(
        software="gjoseph92/profiling",
        n_workers=1,
        worker_cpu=1,
        worker_memory="4 GiB",
        scheduler_cpu=4,
        scheduler_memory="8 GiB",
        shutdown_on_close=True,
        scheduler_options={"idle_timeout": "1 hour"},
    )
    client = distributed.Client(cluster)
    # if not client.run_on_scheduler(lambda: distributed.scheduler.COMPILED):
    #     print("Scheduler is not compiled!")
    #     client.shutdown()
    #     client.close()
    #     sys.exit(1)

    print(f"Waiting for {n_workers} workers...")
    try:
        cluster.scale(n_workers)
    except asyncio.TimeoutError:
        pass
    client.wait_for_workers(n_workers)

    def disable_gc():
        # https://github.com/benfred/py-spy/issues/389#issuecomment-833903190
        import gc

        gc.disable()
        gc.set_threshold(0)

    print("Disabling GC on scheduler")
    client.run_on_scheduler(disable_gc)

    # def enable_gc_debug():
    #     import gc

    #     gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE)

    # print("Enabling GC debug logging on scheduler")
    # client.run_on_scheduler(enable_gc_debug)

    print("Here we go!")

    dask.config.set(
        {
            # This is key---otherwise we're uploading ~300MiB of graph to the scheduler
            "optimization.fuse.active": False,
            # Handle flaky connections to Coiled
            "distributed.comm.retry.count": 5,
        }
    )

    test_name = "purepy-shuffle-nogc-coassign"
    initial_cpu = client.run_on_scheduler(psutil.cpu_times)
    with (
        distributed.performance_report(f"results/{test_name}.html"),
        pyspy_on_scheduler(
            f"results/{test_name}.json",
            subprocesses=True,
            idle=True,
            native=True,
        ),
    ):
        elapsed = main()
        print(f"{elapsed:.1f} sec")

    final_cpu = client.run_on_scheduler(psutil.cpu_times)
    cpu_delta = type(final_cpu)(*(f - i for f, i in zip(final_cpu, initial_cpu)))
    print(
        "CPU times:",
        f"Initial: {initial_cpu}",
        f"Final: {final_cpu}",
        f"Delta: {cpu_delta}",
        sep="\n",
    )

    client.shutdown()
    client.close()
