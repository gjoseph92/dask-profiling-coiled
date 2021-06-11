import asyncio
import sys
import time
import pickle

import coiled
import dask
import dask.utils
import dask.dataframe
import distributed
import distributed.protocol

from scheduler_profilers import pyspy_on_scheduler


def print_sizeof_serialized_graph(x) -> None:
    start = time.perf_counter()
    dsk = dask.base.collections_to_dsk([x], optimize_graph=True)
    optimize_time = time.perf_counter() - start

    start = time.perf_counter()
    packed = dsk.__dask_distributed_pack__(distributed.get_client(), x.__dask_keys__())
    pack_time = time.perf_counter() - start

    start = time.perf_counter()
    frames = distributed.protocol.dumps(packed)
    dumps_time = time.perf_counter() - start
    dumps = sum(len(f) for f in frames)

    start = time.perf_counter()
    pickled = len(pickle.dumps(packed))
    pickle_time = time.perf_counter() - start

    print(
        f"Graph ({len(dsk)} optimized tasks) is:\n"
        f"* {dask.utils.format_bytes(dumps)} with distributed-dumps ({len(frames)} frames) - {dumps_time:.1}s\n"
        f"* {dask.utils.format_bytes(pickled)} pickled  - {pickle_time:.1}s\n"
        f"Optimize: {optimize_time:.1}s, pack: {pack_time:.1}s"
    )


def main():
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
    print(f"{elapsed:.1f} sec")


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
        environ={
            "DASK_DISTRIBUTED__WORKER__BATCHED_SEND_INTERVAL": "60ms"
        }
    )
    client = distributed.Client(cluster)
    if not client.run_on_scheduler(lambda: distributed.scheduler.COMPILED):
        print("Scheduler is not compiled!")
        client.shutdown()
        client.close()
        sys.exit(1)

    client.wait_for_workers(1)
    print(
        client.run(lambda: dask.config.get("distributed.worker.batched-send-interval"))
    )

    print(f"Waiting for {n_workers} workers...")
    try:
        cluster.scale(n_workers)
    except asyncio.TimeoutError:
        pass
    client.wait_for_workers(n_workers)

    # def disable_gc():
    #     # https://github.com/benfred/py-spy/issues/389#issuecomment-833903190
    #     import gc

    #     gc.disable()
    #     gc.set_threshold(0)

    # print("Disabling GC on scheduler")
    # client.run_on_scheduler(disable_gc)

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
            "distributed.comm.retry.count": 5,
        }
    )

    test_name = "cython-shuffle-gc-60ms-batched-send"
    with (
        distributed.performance_report(f"results/{test_name}.html"),
        pyspy_on_scheduler(
            f"results/{test_name}.json",
            subprocesses=True,
            idle=True,
            native=True,
        ),
    ):
        main()

    client.shutdown()
    client.close()
