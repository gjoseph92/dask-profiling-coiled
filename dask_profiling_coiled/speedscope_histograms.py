"""
Plot histograms of runtimes of a function from a speedscope profile.

Meant for use in a REPL, like:
    $ ipython -i dask_profiling_coiled/speedscope_histograms.py
    >>> top_histograms()
    >>> top_histograms(fraction_total_cutoff=1)
    >>> ds = get_durations("handle_task_finished")
    >>> max(ds)
    >>> np.percentile(ds, 99)
    >>> histogram("handle_task_finished")

Looking at the weirdly long tail of some functions is what led to discovering the GC issue.
"""

import json
import operator
from typing import List, Sequence
import itertools
import concurrent.futures

import numpy as np

PROFILE_NAME = "MainThread"


with open("results/cython.json") as f:
    speedscope = json.load(f)

# Parse speedscope format.
# It's basically:
# 1) a list of frames (metadata about function name, file, etc.) in whatever order.
# 2) a list of lists of samples in time order, where each sub-list is the call-stack at that time,
#    and each element is an integer which indexes into the frames list.
# We want to reshape this to be grouped by frame, so for each function, we have a list of all of its runtimes.
# Note that when the same frame is running for multiple samples (as is usually the case), its index just gets repeated
# in the call-stack. So to compute runtime, we just keep summing up consecutive samples until the frame ID at a given
# position in the call-stack changes.

profile = [p for p in speedscope["profiles"] if p["name"] == PROFILE_NAME][0]
samples = profile["samples"]
frames: list = speedscope["shared"]["frames"]
durations: List[List[int]] = [[] for _ in frames]

current_durations = np.zeros(len(frames), dtype=int)
previous_sample: List[int] = samples[0]
for sample in samples[1:]:
    for prev, cur in itertools.zip_longest(previous_sample, sample, fillvalue=None):
        if cur is not None:
            current_durations[cur] += 1
        if prev == cur:
            continue

        if prev is not None:
            # previous frame has ended; record its duration
            prev_duration = current_durations[prev]
            durations[prev].append(prev_duration)
            current_durations[prev] = 0

    previous_sample = sample


def lookup_frame(name: str) -> int:
    for i, frame in enumerate(frames):
        if frame["name"].startswith(name):
            return i
    raise KeyError(name)


def get_durations(name: str) -> List[int]:
    return durations[lookup_frame(name)]


def histogram(name: str, bins=50):
    import matplotlib.pyplot as plt

    durations = get_durations(name)
    plt.hist(durations, bins=bins)
    plt.yscale("log")
    plt.title(name)
    plt.ylabel("Count")
    plt.xlabel("Samples (1/100 sec)")
    plt.show()


def histograms(
    frame_is: Sequence[int],
    durations: Sequence[Sequence[int]] = durations,
    bins=50,
    size=3,
):
    "Plot histograms of frame durations in a grid"
    import matplotlib.pyplot as plt

    n = len(frame_is)
    cols = int(np.sqrt(n))
    rows = int(np.ceil(n / cols))
    fig, subplots = plt.subplots(
        nrows=rows, ncols=cols, tight_layout=True, figsize=(cols * size, rows * size)
    )

    for i, (ax, frame_i) in enumerate(zip(subplots.flat, frame_is)):
        ax: plt.Axes

        frame = frames[frame_i]
        durs = durations[frame_i]
        total_duration = np.sum(durs)

        ax.hist(durs, bins=bins)
        # ax.set_yscale("log")
        ax.set_title(f"{i}: {frame['name']} - {total_duration / 100:.3f} sec")
        ax.set_ylabel("Count")
        ax.set_xlabel("Samples (1/100 sec)")

    fig.show()


def filter_reasonable_durations(durations: List[List[int]], cutoff=0.2):
    """
    Drop frames whose total duration is > ``cutoff`` fraction of the entire sample

    Simple heuristic to drop things like ``run_forever``.
    """
    max_reasonable_total = int(len(durations) * cutoff)
    return [d if sum(d) <= max_reasonable_total else [] for d in durations]


def filter_outlier_durations(durations: List[List[int]], outlier_percentile=95):
    """
    Drop individual durations that are very high for a given frame.

    Simple (probably inaccurate) heuristic to counteract the mysterious "every 10 seconds" pauses,
    which randomly inflate the total time of whatever frames they happen to land on.
    """

    def drop_above_percentile(durs: List[int]):
        if len(durs) == 0:
            return durs
        arr = np.array(durs)
        cutoff = np.percentile(arr, outlier_percentile)
        return arr[arr <= cutoff]

    with concurrent.futures.ThreadPoolExecutor() as exc:
        return list(exc.map(drop_above_percentile, durations))


def top_histograms(
    n=10, fraction_total_cutoff=0.2, outlier_percentile=95, bins=50, size=3
):
    "Plot histograms of the durations of the frames with the highest total times"
    durs = durations
    if fraction_total_cutoff < 1:
        durs = filter_reasonable_durations(durs, cutoff=fraction_total_cutoff)
    if outlier_percentile < 100:
        durs = filter_outlier_durations(durs, outlier_percentile=outlier_percentile)

    total_is_durs = [(i, sum(durs)) for i, durs in enumerate(durs)]
    total_is_durs.sort(key=operator.itemgetter(1), reverse=True)
    top_is, top_total_durs = zip(*total_is_durs[:n])
    histograms(top_is, durs, bins=bins, size=size)
