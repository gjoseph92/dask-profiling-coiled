# Profiling results

Speedscope profiles and dask performance reports of each profiling run.

The filename of a profile _should_ correspond to the name of the commit that produced it.
If you click on the commit name next to the file, you can see that commit and the code.

Most of the variation is from toggling the py-spy `--gil` and `--function` flags
(and `--nonblocking`, just to confirm it wasn't causing the pauses).

`--function` is nice for a bigger-picture look at summary stats (which functions are the slowest?).

`--gil` helped confirm that the GC pauses weren't due to the GIL
(since the pauses showed up in frames that holding the GIL, so clearly they couldn't be waiting on it).
It's also nice for dropping the `select` frames, to filter down to just the frames we're doing work.

Then `gc` vs `nogc` is garbage collection enabled vs disabled on the scheduler.

`cython` and `cython-nogc` are probably the most interesting / simplest to compare.

Additionally, `cython-no-spy-spy` and `cython-nogc-no-spy-spy` are just performance reports with GC on and off,
to get a comparison without py-spy slowing things down.

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

## Results


### cython-function-level
* Performance report: [cython-function-level.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-function-level.html?raw=true)
* Speedscope profile: [cython-function-level.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8%2Fresults%2Fcython-function-level.json%3Fraw%3Dtrue&title=cython-function-level)

### cython-gc-no-py-spy
* Performance report: [cython-gc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-gc-no-py-spy.html?raw=true)

### cython-gil-nogc
* Performance report: [cython-gil-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-gil-nogc.html?raw=true)
* Speedscope profile: [cython-gil-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8%2Fresults%2Fcython-gil-nogc.json%3Fraw%3Dtrue&title=cython-gil-nogc)

### cython-gil-nonblockig
* Performance report: [cython-gil-nonblockig.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-gil-nonblockig.html?raw=true)
* Speedscope profile: [cython-gil-nonblockig.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8%2Fresults%2Fcython-gil-nonblockig.json%3Fraw%3Dtrue&title=cython-gil-nonblockig)

### cython-gil-only-function-level
* Performance report: [cython-gil-only-function-level.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-gil-only-function-level.html?raw=true)
* Speedscope profile: [cython-gil-only-function-level.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8%2Fresults%2Fcython-gil-only-function-level.json%3Fraw%3Dtrue&title=cython-gil-only-function-level)

### cython-gil-only
* Performance report: [cython-gil-only.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-gil-only.html?raw=true)
* Speedscope profile: [cython-gil-only.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8%2Fresults%2Fcython-gil-only.json%3Fraw%3Dtrue&title=cython-gil-only)

### cython-nogc-no-py-spy
* Performance report: [cython-nogc-no-py-spy.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-nogc-no-py-spy.html?raw=true)

### cython-nogc
* Performance report: [cython-nogc.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython-nogc.html?raw=true)
* Speedscope profile: [cython-nogc.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8%2Fresults%2Fcython-nogc.json%3Fraw%3Dtrue&title=cython-nogc)

### cython
* Performance report: [cython.html](https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/e48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8/results/cython.html?raw=true)
* Speedscope profile: [cython.json](https://www.speedscope.app/#profileURL=https%3A%2F%2Frawcdn.githack.com%2Fgjoseph92%2Fdask-profiling-coiled%2Fe48d1e07ff9ab9f61360e04b597d0b58c0e3e2c8%2Fresults%2Fcython.json%3Fraw%3Dtrue&title=cython)
