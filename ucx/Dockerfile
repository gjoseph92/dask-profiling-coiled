ARG BASE_IMAGE=mambaorg/micromamba:0.13.1

FROM $BASE_IMAGE as build

RUN mamba install -y -n base -c conda-forge \
    # Note: keep versions up to date with environment.yml
    python=3.9.1 cython=0.29.22 setuptools git \
    # Remove these later:
    automake make libtool pkg-config libhwloc psutil gcc_linux-64 gxx_linux-64 && \
    mamba clean --all --yes

WORKDIR /root
RUN git clone https://github.com/openucx/ucx && mkdir ucx/build
WORKDIR /root/ucx
RUN ./autogen.sh
RUN ./contrib/configure-release --prefix=$CONDA_PREFIX --enable-debug --enable-mt --disable-cma --disable-numa
RUN make -j install

WORKDIR /root
RUN git clone https://github.com/rapidsai/ucx-py
WORKDIR /root/ucx-py
RUN python -m pip install .

RUN mamba remove -y -n base \
    automake make libtool pkg-config libhwloc psutil gcc_linux-64 gxx_linux-64 && \
    mamba clean --all --yes

FROM $BASE_IMAGE
COPY --from=build /opt/conda /opt/conda
WORKDIR /root

# Install environment.yml
# We'd like to let Coiled do this for us, but it's not currently possible with micromamba
# because of https://github.com/coiled/cloud/issues/2910
COPY environment.yml /root/environment.yml
RUN sed "s/name: profiling/name: base/" environment.yml
# Workaround for https://github.com/mamba-org/mamba/issues/1005:
# separate out the `pip` section into its own `requirements.txt` file
RUN csplit --suppress-matched environment.yml '/- pip:/' '{*}' && \
    mv xx00 environment.yml && \
    sed "s/ - //" xx01 > requirements.txt && \
    rm xx01
RUN mamba env update -n base -f environment.yml && \
    mamba clean --all --yes && \
    rm environment.yml
RUN python3 -m pip install -r requirements.txt && \
    rm requirements.txt
RUN python3 -m pip install git+https://github.com/gjoseph92/scheduler-profilers.git@2691c0fc79e4f4fc9e90c7cfcbdf153f45107d36

# # Uncomment to test using security locally
# ADD ucx/generate_security.py /root/generate_security.py
# RUN python generate_security.py > security.txt && rm generate_security.py
# ENV DASK_DISTRIBUTED__COMM__TLS__CA_FILE=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__CLIENT__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__CLIENT__KEY=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__SCHEDULER__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__SCHEDULER__KEY=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__WORKER__CERT=security.txt \
#     DASK_DISTRIBUTED__COMM__TLS__WORKER__KEY=security.txt