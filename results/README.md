# Profiling results

Speedscope profiles and dask performance reports of each profiling run.
For all speedscope profiles, you want to look at `MainThread`.

The filename of a profile _should_ correspond to the name of the commit that produced it.
If you click on the commit name next to the file, you can see that commit and the code.

Most of the variation is from toggling the py-spy `--gil` and `--function` flags
(and `--nonblocking`, just to confirm it wasn't causing the pauses).

`--function` is nice for a bigger-picture look at summary stats (which functions are the slowest?).

`--gil` helped confirm that the GC pauses weren't due to the GIL
(since the pauses showed up in frames that holding the GIL, so clearly they couldn't be waiting on it).
It's also nice for dropping the `select` frames, to filter down to just the frames we're doing work.

Then `gc` vs `nogc` is garbage collection enabled vs disabled on the scheduler.

Quick reference for what the py-spy options do:
```shell
$ py-spy record -h
py-spy-record
Records stack trace information to a flamegraph, speedscope or raw file

USAGE:
    py-spy record [OPTIONS] --pid <pid> [python_program]...

OPTIONS:
    -p, --pid <pid>              PID of a running python program to spy on
        --full-filenames         Show full Python filenames, instead of shortening to show only the package part
    -o, --output <filename>      Output filename
    -f, --format <format>        Output file format [default: flamegraph]  [possible values: flamegraph, raw, speedscope]
    -d, --duration <duration>    The number of seconds to sample for [default: unlimited]
    -r, --rate <rate>            The number of samples to collect per second [default: 100]
    -s, --subprocesses           Profile subprocesses of the original process
    -F, --function               Aggregate samples by function name instead of by line number
    -g, --gil                    Only include traces that are holding on to the GIL
    -t, --threads                Show thread ids in the output
    -i, --idle                   Include stack traces for idle threads
        --nonblocking            Don't pause the python process when collecting samples. Setting this option will reduce the perfomance impact of sampling, but may lead to inaccurate results
    -h, --help                   Prints help information
    -V, --version                Prints version information

ARGS:
    <python_program>...    commandline of a python program to run
```

## What to look at

`cython-shuffle-nogc` is the most canonical profile of what we're spending time on right now.

`cython-shuffle-gc` and `cython-shuffle-nogc` are probably the most interesting to compare,
showing the impact of garbage collection.

`cython-shuffle-gc-nopyspy` vs `2.30-shuffle-gc-nopyspy` (and `cython-shuffle-nogc-nopyspy` vs `2.30-shuffle-nogc-nopyspy`)
are the canonical "before-after" comparison showing improvements in scheduler performance since version 2.30.0.

Additionally, `cython-shuffle-gc-nopyspy` and `cython-shuffle-nogc-nopyspy` are just performance reports with GC on and off,
to get a comparison of GC impact without py-spy slowing things down.

## Results


### 2.30-shuffle-gc-nopyspy
* Performance report: [2.30-shuffle-gc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/2.30-shuffle-gc-nopyspy.html?raw=true)

### 2.30-shuffle-gc
* Performance report: [2.30-shuffle-gc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/2.30-shuffle-gc.html?raw=true)
* Speedscope profile: [2.30-shuffle-gc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2F2.30-shuffle-gc.json%3Fraw%3Dtrue)

### 2.30-shuffle-nogc-nopyspy
* Performance report: [2.30-shuffle-nogc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/2.30-shuffle-nogc-nopyspy.html?raw=true)

### 2.30-shuffle-nogc
* Performance report: [2.30-shuffle-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/2.30-shuffle-nogc.html?raw=true)
* Speedscope profile: [2.30-shuffle-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2F2.30-shuffle-nogc.json%3Fraw%3Dtrue)

### cython-function-level
* Performance report: [cython-function-level.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-function-level.html?raw=true)
* Speedscope profile: [cython-function-level.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-function-level.json%3Fraw%3Dtrue)

### cython-gc-no-py-spy
* Performance report: [cython-gc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-gc-no-py-spy.html?raw=true)

### cython-gil-nogc
* Performance report: [cython-gil-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-gil-nogc.html?raw=true)
* Speedscope profile: [cython-gil-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-gil-nogc.json%3Fraw%3Dtrue)

### cython-gil-nonblockig
* Performance report: [cython-gil-nonblockig.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-gil-nonblockig.html?raw=true)
* Speedscope profile: [cython-gil-nonblockig.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-gil-nonblockig.json%3Fraw%3Dtrue)

### cython-gil-only-function-level
* Performance report: [cython-gil-only-function-level.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-gil-only-function-level.html?raw=true)
* Speedscope profile: [cython-gil-only-function-level.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-gil-only-function-level.json%3Fraw%3Dtrue)

### cython-gil-only
* Performance report: [cython-gil-only.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-gil-only.html?raw=true)
* Speedscope profile: [cython-gil-only.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-gil-only.json%3Fraw%3Dtrue)

### cython-nogc-no-py-spy
* Performance report: [cython-nogc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-nogc-no-py-spy.html?raw=true)

### cython-nogc
* Performance report: [cython-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-nogc.html?raw=true)
* Speedscope profile: [cython-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-nogc.json%3Fraw%3Dtrue)

### cython-shuffle-gc-debug-noprofiling-ecs-prod-nopyspy
* Logs: [cython-shuffle-gc-debug-noprofiling-ecs-prod-nopyspy.txt](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-gc-debug-noprofiling-ecs-prod-nopyspy.txt?raw=true)

### cython-shuffle-gc-debug-noprofiling
* Performance report: [cython-shuffle-gc-debug-noprofiling.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-gc-debug-noprofiling.html?raw=true)
* Speedscope profile: [cython-shuffle-gc-debug-noprofiling.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-shuffle-gc-debug-noprofiling.json%3Fraw%3Dtrue)

### cython-shuffle-gc-noprofiling-daskconfig
* Performance report: [cython-shuffle-gc-noprofiling-daskconfig.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-gc-noprofiling-daskconfig.html?raw=true)
* Speedscope profile: [cython-shuffle-gc-noprofiling-daskconfig.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-shuffle-gc-noprofiling-daskconfig.json%3Fraw%3Dtrue)

### cython-shuffle-gc-noprofiling-env
* Performance report: [cython-shuffle-gc-noprofiling-env.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-gc-noprofiling-env.html?raw=true)
* Speedscope profile: [cython-shuffle-gc-noprofiling-env.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-shuffle-gc-noprofiling-env.json%3Fraw%3Dtrue)

### cython-shuffle-gc-nopyspy
* Performance report: [cython-shuffle-gc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-gc-nopyspy.html?raw=true)

### cython-shuffle-gc
* Performance report: [cython-shuffle-gc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-gc.html?raw=true)
* Speedscope profile: [cython-shuffle-gc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-shuffle-gc.json%3Fraw%3Dtrue)

### cython-shuffle-nogc-nopyspy
* Performance report: [cython-shuffle-nogc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-nogc-nopyspy.html?raw=true)

### cython-shuffle-nogc
* Performance report: [cython-shuffle-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-nogc.html?raw=true)
* Speedscope profile: [cython-shuffle-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython-shuffle-nogc.json%3Fraw%3Dtrue)

### cython-shuffle-uvloop-gc-debug-noprofiling-ecs-prod-nopyspy
* Logs: [cython-shuffle-uvloop-gc-debug-noprofiling-ecs-prod-nopyspy.txt](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-uvloop-gc-debug-noprofiling-ecs-prod-nopyspy.txt?raw=true)

### cython-shuffle-uvloop-gc-noprofiling-ecs-prod-nopyspy
* Performance report: [cython-shuffle-uvloop-gc-noprofiling-ecs-prod-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython-shuffle-uvloop-gc-noprofiling-ecs-prod-nopyspy.html?raw=true)

### cython
* Performance report: [cython.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/cython.html?raw=true)
* Speedscope profile: [cython.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fcython.json%3Fraw%3Dtrue)

### purepy-gc-no-py-spy
* Performance report: [purepy-gc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/purepy-gc-no-py-spy.html?raw=true)

### purepy-gc
* Performance report: [purepy-gc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/purepy-gc.html?raw=true)
* Speedscope profile: [purepy-gc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fpurepy-gc.json%3Fraw%3Dtrue)

### purepy-nogc-no-py-spy
* Performance report: [purepy-nogc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/purepy-nogc-no-py-spy.html?raw=true)

### purepy-nogc
* Performance report: [purepy-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e3f25ec3551193e7432d87fd24b140cd3738782b/results/purepy-nogc.html?raw=true)
* Speedscope profile: [purepy-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe3f25ec3551193e7432d87fd24b140cd3738782b%2Fresults%2Fpurepy-nogc.json%3Fraw%3Dtrue)
