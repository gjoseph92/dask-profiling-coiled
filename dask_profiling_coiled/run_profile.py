import asyncio
import sys
import time
from typing import Dict, cast, Tuple

import coiled
import dask
import dask.utils
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
    r = client.run_on_scheduler(
        lambda: (psutil.cpu_times()._asdict(), psutil.Process().memory_info()._asdict())
    )
    initial_cpu, initial_mem = cast(Tuple[Dict[str, float], Dict[str, float]], r)

    with distributed.performance_report(f"results/benchmarks/{test_name}-{i}.html"):
        elapsed = main()
        r = client.run_on_scheduler(
            lambda: (
                psutil.cpu_times()._asdict(),
                psutil.Process().memory_info()._asdict(),
            )
        )
        final_cpu, final_mem = cast(Tuple[Dict[str, float], Dict[str, float]], r)

    cpu_delta = {k: v - initial_cpu[k] for k, v in final_cpu.items()}
    mem_delta = {k: v - initial_mem[k] for k, v in final_mem.items()}
    cpu_count = client.run_on_scheduler(psutil.cpu_count)

    def formatted(mem_info: dict) -> dict:
        return {k: dask.utils.format_bytes(v) for k, v in mem_info.items()}

    print(f"[bold]{elapsed:.1f} sec")
    print(
        "[underline]CPU times:[/]",
        f"Initial: {initial_cpu}",
        f"Final: {final_cpu}",
        f"Delta: {cpu_delta}",
        "[underline]Memory:[/]",
        f"Initial: {formatted(initial_mem)}",
        f"Final: {formatted(final_mem)}",
        f"Delta: {formatted(mem_delta)}",
        sep="\n",
    )

    def prefix(p: str, d: dict) -> dict:
        return {p + k: v for k, v in d.items()}

    return {
        "elapsed": elapsed,
        **cpu_delta,
        "cpu_count": cpu_count,
        **prefix("initial-", initial_mem),
        **prefix("final-", final_mem),
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
#         environ={"MALLOC_TRIM_THRESHOLD_": "0"},
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
    test_name = "purepy-shuffle-nogc-notrim"
    trials = []
    try:
        for i in range(n_trials):
            trials.append(trial(client, i))
    except BaseException:
        print(trials)
        raise

    print("[bold green]Trials complete!")

    print(trials)

    df = pd.DataFrame.from_records(trials).rename_axis("trial")
    df.to_csv(f"results/benchmarks/{test_name}.csv")

    client.shutdown()
