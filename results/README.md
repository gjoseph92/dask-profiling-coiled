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
* Performance report: [2.30-shuffle-gc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/996a922b654ed6553bb25f2f55793ef5512772af/results/2.30-shuffle-gc-nopyspy.html?raw=true)

### 2.30-shuffle-gc
* Performance report: [2.30-shuffle-gc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/b7861f03d1f06c94040103d78e758e0a677cae32/results/2.30-shuffle-gc.html?raw=true)
* Speedscope profile: [2.30-shuffle-gc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fb7861f03d1f06c94040103d78e758e0a677cae32%2Fresults%2F2.30-shuffle-gc.json%3Fraw%3Dtrue)

### 2.30-shuffle-nogc-nopyspy
* Performance report: [2.30-shuffle-nogc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/7cf63d4e62894fb08f64eb3af8c3c7da1d952d44/results/2.30-shuffle-nogc-nopyspy.html?raw=true)

### 2.30-shuffle-nogc
* Performance report: [2.30-shuffle-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/0a374786573df9415142e5d2c3668199f29c91ae/results/2.30-shuffle-nogc.html?raw=true)
* Speedscope profile: [2.30-shuffle-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F0a374786573df9415142e5d2c3668199f29c91ae%2Fresults%2F2.30-shuffle-nogc.json%3Fraw%3Dtrue)

### cython-function-level
* Performance report: [cython-function-level.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/b137e5ffe4b78f4908abe4921f78c4deb029238d/results/cython-function-level.html?raw=true)
* Speedscope profile: [cython-function-level.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fb137e5ffe4b78f4908abe4921f78c4deb029238d%2Fresults%2Fcython-function-level.json%3Fraw%3Dtrue)

### cython-gc-no-py-spy
* Performance report: [cython-gc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/1fd7865950a29140c879eafde7f74e5d6fa8926a/results/cython-gc-no-py-spy.html?raw=true)

### cython-gil-nogc
* Performance report: [cython-gil-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/ad353203ee48a336c8abfe22a6aa1a13aa89ff5a/results/cython-gil-nogc.html?raw=true)
* Speedscope profile: [cython-gil-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fad353203ee48a336c8abfe22a6aa1a13aa89ff5a%2Fresults%2Fcython-gil-nogc.json%3Fraw%3Dtrue)

### cython-gil-nonblockig
* Performance report: [cython-gil-nonblockig.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e30f494a2cd5b83cf6c6b4182b2bc5a0ce4ab88d/results/cython-gil-nonblockig.html?raw=true)
* Speedscope profile: [cython-gil-nonblockig.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe30f494a2cd5b83cf6c6b4182b2bc5a0ce4ab88d%2Fresults%2Fcython-gil-nonblockig.json%3Fraw%3Dtrue)

### cython-gil-only-function-level
* Performance report: [cython-gil-only-function-level.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/6c38be1a5e284c3227d7fbc4b7731402002de091/results/cython-gil-only-function-level.html?raw=true)
* Speedscope profile: [cython-gil-only-function-level.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F6c38be1a5e284c3227d7fbc4b7731402002de091%2Fresults%2Fcython-gil-only-function-level.json%3Fraw%3Dtrue)

### cython-gil-only
* Performance report: [cython-gil-only.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/0469d942a37096c9299b119f0767d8d59890d816/results/cython-gil-only.html?raw=true)
* Speedscope profile: [cython-gil-only.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F0469d942a37096c9299b119f0767d8d59890d816%2Fresults%2Fcython-gil-only.json%3Fraw%3Dtrue)

### cython-nogc-no-py-spy
* Performance report: [cython-nogc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/0731fc9c59f76068b592077dc7fbee89a7be36ba/results/cython-nogc-no-py-spy.html?raw=true)

### cython-nogc
* Performance report: [cython-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/f08c91870ecb5b2c9621ec1145499eaae16e26e5/results/cython-nogc.html?raw=true)
* Speedscope profile: [cython-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Ff08c91870ecb5b2c9621ec1145499eaae16e26e5%2Fresults%2Fcython-nogc.json%3Fraw%3Dtrue)

### cython-shuffle-distributed4847-2
* Performance report: [cython-shuffle-distributed4847-2.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/0695c0ce92887ce9a552b0e71c62c9b9582731b1/results/cython-shuffle-distributed4847-2.html?raw=true)
* Speedscope profile: [cython-shuffle-distributed4847-2.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F0695c0ce92887ce9a552b0e71c62c9b9582731b1%2Fresults%2Fcython-shuffle-distributed4847-2.json%3Fraw%3Dtrue)

### cython-shuffle-distributed4847
* Performance report: [cython-shuffle-distributed4847.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/ec9099b731352937aaa7779e90c19bd5702125f0/results/cython-shuffle-distributed4847.html?raw=true)
* Speedscope profile: [cython-shuffle-distributed4847.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fec9099b731352937aaa7779e90c19bd5702125f0%2Fresults%2Fcython-shuffle-distributed4847.json%3Fraw%3Dtrue)

### cython-shuffle-gc-debug-noprofiling-ecs-prod-nopyspy
* Logs: [cython-shuffle-gc-debug-noprofiling-ecs-prod-nopyspy.txt](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/61fc875173a5b2f9195346f2a523cb1d876c48ad/results/cython-shuffle-gc-debug-noprofiling-ecs-prod-nopyspy.txt?raw=true)

### cython-shuffle-gc-debug-noprofiling
* Performance report: [cython-shuffle-gc-debug-noprofiling.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/c0ea2aa1dd2064f5e69cbe21da7209ee9884055c/results/cython-shuffle-gc-debug-noprofiling.html?raw=true)
* Speedscope profile: [cython-shuffle-gc-debug-noprofiling.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fc0ea2aa1dd2064f5e69cbe21da7209ee9884055c%2Fresults%2Fcython-shuffle-gc-debug-noprofiling.json%3Fraw%3Dtrue)

### cython-shuffle-gc-noprofiling-daskconfig
* Performance report: [cython-shuffle-gc-noprofiling-daskconfig.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/f8721be3ff0478a94ffca27dac2a05ea23e28455/results/cython-shuffle-gc-noprofiling-daskconfig.html?raw=true)
* Speedscope profile: [cython-shuffle-gc-noprofiling-daskconfig.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Ff8721be3ff0478a94ffca27dac2a05ea23e28455%2Fresults%2Fcython-shuffle-gc-noprofiling-daskconfig.json%3Fraw%3Dtrue)

### cython-shuffle-gc-noprofiling-env
* Performance report: [cython-shuffle-gc-noprofiling-env.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/ac61e5f824fe392b9e71e0cbedb251f02b5fafc2/results/cython-shuffle-gc-noprofiling-env.html?raw=true)
* Speedscope profile: [cython-shuffle-gc-noprofiling-env.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fac61e5f824fe392b9e71e0cbedb251f02b5fafc2%2Fresults%2Fcython-shuffle-gc-noprofiling-env.json%3Fraw%3Dtrue)

### cython-shuffle-gc-nopyspy
* Performance report: [cython-shuffle-gc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/a55514d0bd0d5f4997db0dfe70240979ef8f972e/results/cython-shuffle-gc-nopyspy.html?raw=true)

### cython-shuffle-gc
* Performance report: [cython-shuffle-gc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/0097f51c50de405d34ea59d40f36520ff27f962b/results/cython-shuffle-gc.html?raw=true)
* Speedscope profile: [cython-shuffle-gc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F0097f51c50de405d34ea59d40f36520ff27f962b%2Fresults%2Fcython-shuffle-gc.json%3Fraw%3Dtrue)

### cython-shuffle-nogc-nopyspy
* Performance report: [cython-shuffle-nogc-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/b941cc39f17060cba61eddf668e744c850d2f054/results/cython-shuffle-nogc-nopyspy.html?raw=true)

### cython-shuffle-nogc
* Performance report: [cython-shuffle-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/48d3b6aa8068e59fd63b8a1adcfbb21795907811/results/cython-shuffle-nogc.html?raw=true)
* Speedscope profile: [cython-shuffle-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F48d3b6aa8068e59fd63b8a1adcfbb21795907811%2Fresults%2Fcython-shuffle-nogc.json%3Fraw%3Dtrue)

### cython-shuffle-uvloop-gc-debug-noprofiling-ecs-prod-nopyspy
* Logs: [cython-shuffle-uvloop-gc-debug-noprofiling-ecs-prod-nopyspy.txt](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/1941a3b438a9eeab1c392241e8c16a91d1848201/results/cython-shuffle-uvloop-gc-debug-noprofiling-ecs-prod-nopyspy.txt?raw=true)

### cython-shuffle-uvloop-gc-noprofiling-ecs-prod-nopyspy
* Performance report: [cython-shuffle-uvloop-gc-noprofiling-ecs-prod-nopyspy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/ef9d42ff44938be4c9abb0dd14c536b194017675/results/cython-shuffle-uvloop-gc-noprofiling-ecs-prod-nopyspy.html?raw=true)

### cython
* Performance report: [cython.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/f2c077c995075275bd05cfe1e42169c6b8ce22ba/results/cython.html?raw=true)
* Speedscope profile: [cython.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Ff2c077c995075275bd05cfe1e42169c6b8ce22ba%2Fresults%2Fcython.json%3Fraw%3Dtrue)

### purepy-gc-no-py-spy
* Performance report: [purepy-gc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/b7dd77278ef7975f6cd55dbc993b461ac19c71d4/results/purepy-gc-no-py-spy.html?raw=true)

### purepy-gc
* Performance report: [purepy-gc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/98e48fc67bc0a0e5c36b6bba18862ae4b081f099/results/purepy-gc.html?raw=true)
* Speedscope profile: [purepy-gc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F98e48fc67bc0a0e5c36b6bba18862ae4b081f099%2Fresults%2Fpurepy-gc.json%3Fraw%3Dtrue)

### purepy-nogc-no-py-spy
* Performance report: [purepy-nogc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/f6989f598ae3fe14cc9e3a2c1c776aa7504b2df5/results/purepy-nogc-no-py-spy.html?raw=true)

### purepy-nogc
* Performance report: [purepy-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/69c38f559af0d2adbf41b3e77892d58221dc992c/results/purepy-nogc.html?raw=true)
* Speedscope profile: [purepy-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2F69c38f559af0d2adbf41b3e77892d58221dc992c%2Fresults%2Fpurepy-nogc.json%3Fraw%3Dtrue)
