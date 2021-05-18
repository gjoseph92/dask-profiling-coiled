#!/bin/bash

sudo dask-scheduler &
SCHEDULER_PID=$!
echo "Scheduler PID: $SCHEDULER_PID"
sleep 1

N_WORKERS=7
for _ in $(seq $N_WORKERS); do
    dask-worker --no-dashboard --nthreads 1 tcp://192.168.0.39:8786 &
done

python dask_profiling_coiled/run_profile.py
sudo kill $SCHEDULER_PID  # workers should stop too
