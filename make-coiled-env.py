#!/usr/bin/env python3

import coiled

if __name__ == "__main__":
    coiled.create_software_environment(
        name="gjoseph92/profiling",
        container="jabriel/ucx:latest",
        conda_env_name="base",
        conda="environment.yml",
        # Install py-spy separately so it doesn't conflict with Cythonized distributed
        post_build=[
            "python3 -m pip install git+https://github.com/gjoseph92/scheduler-profilers.git@2691c0fc79e4f4fc9e90c7cfcbdf153f45107d36"  # noqa: E501
        ],
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
