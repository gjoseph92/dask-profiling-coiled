# Running with UCX

NOTE: UCX isn't currently working on Coiled.

Local testing:

```bash
$ cd ucx
$ docker pull jabriel/ucx:full
$ docker compose up  # start scheduler, 2 workers, and a Python REPL client. Also open localhost:8787 to see dashboard.
$ docker attach dask-profiling-coiled_client_1
>>> da.random.random(1000000, chunks=1000).mean().compute()  # test a computation
```

### Building the image

From the root directory:
```bash
docker build -t jabriel/ucx:full -f ucx/Dockerfile .
```