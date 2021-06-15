#!/usr/bin/env python3

import subprocess

import coiled

if __name__ == "__main__":
    # Get image with its SHA
    # https://stackoverflow.com/a/33511811
    img = subprocess.run(
        "docker inspect --format='{{index .RepoDigests 0}}' jabriel/ucx:full",
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    print(f"Using {img}")

    coiled.create_software_environment(
        name="gjoseph92/profiling",
        container=img,
    )

    coiled.create_job_configuration(
        name="profiling",
        software="gjoseph92/profiling",
        cpu=2,
        memory="4 GiB",
        command=[
            "/bin/bash",
            "-c",
            "SHELL=/bin/bash jupyter lab --allow-root --ip=0.0.0.0 --no-browser",
        ],
        ports=[8888],
        files=["dask_profiling_coiled/run_profile.py"],
    )
