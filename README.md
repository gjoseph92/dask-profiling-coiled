# Dask scheduler profiling on Coiled

Script for (and results of) profiling the [dask distributed](https://github.com/dask/distributed) scheduler using the [py-spy](https://github.com/benfred/py-spy) statistical profiler on [Coiled](https://coiled.io/).

The goal is to profile the scheduler running a scheduler-bound workload on a large multi-machine cluster. For the cluster, we use Coiled to spin up a 100-worker cluster on 100 separate VMs. For the workload, we run a distributed shuffle of a synthetic dataframe.

## Reproducing

**NOTE:** currently (2021-05-14), this can only run on Coiled's staging environment. Within a week or two, this should work for any Coiled user.

```shell
git clone git@github.com:gjoseph92/dask-profiling-coiled.git
cd dask-profiling-coiled
mamba env create -f environment.yml  # creates a conda environment named `profiling`
conda activate profiling
# you have to install this manually, since py-spy only has wheels, and building Cythonized distributed
# makes pip refuse to install from wheels
pip install git+https://github.com/gjoseph92/scheduler-profilers.git
```

On <https://cloud.coiled.io/>, go to the Account page, and change your backend to AWS VMs (EC2).

To run:

Adjust settings as you like in the `profile.py` script. Make sure to update `test_name` so you don't overwrite old outputs. Then:
```
python dask_profiling_coiled/profile.py
```
This will take 5-8 minutes, and produce a dask performance report and a speedscope JSON file which you can view in <https://speedscope.app/>.
