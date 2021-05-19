"""
Generate the README with links to all results on githack/speedscope.

python results/make-readme.py > results/README.md
"""
import itertools
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote_plus

readme = """\
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
"""  # noqa: E501

commit = subprocess.run(
    ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
).stdout.strip()


def githack_link(path: Path):
    return f"https://rawcdn.githack.com/gjoseph92/dask-profiling-coiled/{commit}/results/{path.name}?raw=true"


def speedscope_link(path: Path):
    return f"https://www.speedscope.app/#profileURL={quote_plus(githack_link(path))}"


dir = Path(__file__).parent
htmls = dir.glob("*.html")
jsons = dir.glob("*.json")
txts = dir.glob("*.txt")
parts = []
for name, items in itertools.groupby(
    sorted(itertools.chain(htmls, jsons, txts)), key=lambda p: p.stem
):
    parts.append(f"\n### {name}")
    for item in items:
        if item.suffix == ".json":
            parts.append(
                f"* Speedscope profile: [{item.name}]({speedscope_link(item)})"
            )
        elif item.suffix == ".html":
            parts.append(f"* Performance report: [{item.name}]({githack_link(item)})")
        elif item.suffix == ".txt":
            parts.append(f"* Logs: [{item.name}]({githack_link(item)})")
        else:
            print(f"What is {item} doing here?", file=sys.stderr)

print(readme, *parts, sep="\n")
