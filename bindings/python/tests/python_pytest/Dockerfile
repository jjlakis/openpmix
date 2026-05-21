# PMIx version must (should?) match the OMPI version of the client

ARG PMIX_REPO=https://github.com/openpmix/openpmix.git
ARG PMIX_REV=master

# Stage 1: build OpenPMIx + Python bindings
FROM ubuntu:24.04 AS pmix-build

RUN apt-get update && apt-get install -y --no-install-recommends \
    git autoconf libtool build-essential perl \
    flex libevent-dev libhwloc-dev zlib1g-dev \
    python3 python3-pip python3-dev \
    && rm -rf /var/lib/apt/lists/*

ARG PMIX_REPO
ARG PMIX_REV

RUN git clone ${PMIX_REPO} /openpmix

WORKDIR /openpmix
RUN git checkout ${PMIX_REV}
RUN git submodule update --init
RUN ./autogen.pl

RUN pip3 install --break-system-packages cython setuptools aiohttp
RUN ./configure --prefix=/opt/pmix --enable-python-bindings
RUN make -j$(nproc) && make install
RUN cp /openpmix/bindings/python/build/lib.linux-x86_64-cpython-312/*.so /usr/lib/python3/dist-packages/ 

# Stage 2: Runtime
FROM python:3.12-slim as runtime

COPY . /test
WORKDIR /test

COPY --from=pmix-build /usr/lib/python3/dist-packages/pmix* /usr/lib/python3/dist-packages/
COPY --from=pmix-build /opt/pmix /opt/pmix

RUN apt-get update && apt-get install -y --no-install-recommends \
    libevent-dev libhwloc-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r /test/requirements.txt --break-system-packages

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/lib/python3/dist-packages
ENV LD_LIBRARY_PATH=/opt/pmix/lib:$LD_LIBRARY_PATH

CMD ["pytest", "-sv"]

