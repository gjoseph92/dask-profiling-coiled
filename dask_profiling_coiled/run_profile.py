import asyncio
import sys
import time

import coiled
import dask
import dask.dataframe
import distributed
import pandas as pd
import psutil
from rich import print


def main() -> float:
    df = dask.datasets.timeseries(
        start="2000-01-01",
        end="2000-06-30",  # 720 ~partitions
        partition_freq="1h",
        freq="60s",
    )
    shuffled = df.shuffle("id", shuffle="tasks")

    start = time.perf_counter()
    df2 = shuffled.persist()
    distributed.wait(df2)
    elapsed = time.perf_counter() - start
    return elapsed


def trial(client: distributed.Client, i: int) -> dict:
    initial_cpu = client.run_on_scheduler(lambda: psutil.cpu_times()._asdict())

    with distributed.performance_report(f"results/benchmarks/{test_name}-{i}.html"):
        elapsed = main()
        final_cpu = client.run_on_scheduler(lambda: psutil.cpu_times()._asdict())

    cpu_delta = {k: v - initial_cpu[k] for k, v in final_cpu.items()}
    cpu_count = client.run_on_scheduler(psutil.cpu_count)

    print(f"[bold]{elapsed:.1f} sec")
    print(
        "CPU times:",
        f"Initial: {initial_cpu}",
        f"Final: {final_cpu}",
        f"Delta: {cpu_delta}",
        sep="\n",
    )

    return {
        "elapsed": elapsed,
        **cpu_delta,
        cpu_count: cpu_count,
    }


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
        environ={"MALLOC_TRIM_THRESHOLD_": "0"},
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

    print("[bold green]Here we go!")

    dask.config.set(
        {
            # This is key---otherwise we're uploading ~300MiB of graph to the scheduler
            "optimization.fuse.active": False,
            # Handle flaky connections to Coiled
            "distributed.comm.retry.count": 5,
        }
    )

    n_trials = 10
    test_name = "purepy-shuffle-nogc-norestart-malloctrim"
    trials = [trial(client, i) for i in range(n_trials)]

    print("[bold green]Trials complete!")

    print(trials)

    df = pd.DataFrame.from_records(trials)
    df.to_csv(f"results/benchmarks/{test_name}.csv")

    client.shutdown()
