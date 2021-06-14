ARG BASE_IMAGE=mambaorg/micromamba:0.13.1

FROM $BASE_IMAGE as build

RUN mamba install -y -n base -c conda-forge \
    # Note: keep versions up to date with environment.yml
    python=3.9.1 cython=0.29.22 setuptools git \
    # Remove these later:
    automake make libtool pkg-config libhwloc psutil gcc_linux-64 gxx_linux-64 && \
    mamba clean --all --yes

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

RUN mamba remove -y -n base \
    automake make libtool pkg-config libhwloc psutil gcc_linux-64 gxx_linux-64 && \
    mamba clean --all --yes

FROM $BASE_IMAGE
COPY --from=build /opt/conda /opt/conda
WORKDIR /home/root

# # Uncomment to install environment for local testing (otherwise we let Coiled do this for us)
# COPY environment.yml /home/root/environment.yml
# RUN sed "s/name: profiling/name: base/" environment.yml
# RUN mamba env update -n base -f environment.yml && \
#     mamba clean --all --yes && \
#     rm environment.yml

# # Uncomment to test using security locally
# ADD generate_security.py /home/root/generate_security.py
# RUN python generate_security.py > security.txt && rm generate_security.py
# ENV DASK_DISTRIBUTED__COMM__TLS__CLIENT__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__CLIENT__KEY=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__SCHEDULER__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__SCHEDULER__KEY=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__WORKER__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__WORKER__KEY=security.txt