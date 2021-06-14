#!/usr/bin/env python3

import coiled

if __name__ == "__main__":
    coiled.create_software_environment(
        name="gjoseph92/profiling",
        container="jabriel/ucx:full",
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
