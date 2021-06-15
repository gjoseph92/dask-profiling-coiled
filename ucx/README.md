# Running with UCX

NOTE: UCX isn't currently working on Coiled.

## Running profiles in docker-compose

```bash
$ cd ucx
$ docker-compose up --scale worker=<N workers> --abort-on-container-exit
```

This will spin up the workers, run the profiling script, save the profile, and exit. Make sure to update the `n_workers` and `test_name` lines in the `run_profile.py` script first. (If just testing on a laptop, also make the `dask.datasets.timeseries` smaller with something like `end="2000-01-05"`, otherwise it'll take forever to run.) Profile results will be saved to the host machine.

## Local testing:

Comment out the `profile` service and uncomment `client` in the docker-compose. Then:

```bash
$ cd ucx
$ docker compose up  # start scheduler, worker, and an IPython REPL client. Also open https://localhost:8787 to see dashboard.
$ docker attach ucx_client_1
>>> da.random.random(1000000, chunks=1000).mean().compute()  # test a computation
```
Use `ctrl-p` `ctrl-q` (Docker escape sequence) to get back to your terminal without exiting the client container.

## Building the image

From the root directory:
```bash
docker build -t jabriel/ucx:full -f ucx/Dockerfile .
```