FROM condaforge/mambaforge:4.10.1-0

RUN mamba install -y -n base -c conda-forge \
    automake make libtool pkg-config cython setuptools libhwloc psutil git gcc_linux-64 gxx_linux-64 && \
    mamba clean --all --yes

# Make RUN commands use the new environment
# https://pythonspeed.com/articles/activate-conda-dockerfile/
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
WORKDIR /home/root
RUN git clone https://github.com/openucx/ucx && mkdir ucx/build
WORKDIR /home/root/ucx
RUN ./autogen.sh
RUN ./contrib/configure-release --prefix=$CONDA_PREFIX --enable-debug --enable-mt --disable-cma --disable-numa
RUN make -j install

WORKDIR /home/root
RUN git clone https://github.com/rapidsai/ucx-py
WORKDIR /home/root/ucx-py
RUN python -m pip install .

WORKDIR /home/root
RUN rm -rf ucx ucx-py

# Uncomment to install environment for local testing (otherwise we let Coiled do this for us)
# COPY environment.yml /home/root/environment.yml
# RUN mamba env update -n base -f environment.yml && \
#     mamba clean --all --yes && \
#     rm environment.yml

# Uncomment to test using security locally
# ADD generate_security.py /home/root/generate_security.py
# RUN python generate_security.py security.txt && rm generate_security.py
# ENV DASK_DISTRIBUTED__COMM__TLS__CLIENT__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__CLIENT__KEY=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__SCHEDULER__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__SCHEDULER__KEY=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__WORKER__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__WORKER__KEY=security.txt