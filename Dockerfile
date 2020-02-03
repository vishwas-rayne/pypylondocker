# basler_test base Dockerfile
FROM ubuntu:18.04
LABEL description="Basler test"

ARG DEBIAN_FRONTEND=noninteractive

# Installing python 2, pip2, python 3.6 and pip3.6
RUN apt-get update && \
    apt-get install -y software-properties-common pkg-config python python-pip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.6 python3.6-dev python3-distutils && \
    apt-get install -y wget && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.6 get-pip.py && \
    apt-get install -y libsm6 libxext6 libfontconfig1 libxrender1

RUN apt-get install -y git

RUN apt-get install -y swig3.0

# Adding basler camera's essentials by referring it's repo's README and Removing unwanted files
RUN wget https://www.baslerweb.com/media/downloads/software/pylon_software/pylon-5.1.0.12682-x86_64.tar.gz && \
    tar xvf pylon-5.1.0.12682-x86_64.tar.gz && \
    cd pylon-5.1.0.12682-x86_64 && \
    pip3.6 install numpy==1.14.5 && \
    pip3.6 install setuptools==40.7.3 && \
    tar -C /opt -zxf pylonSDK-5.1.0.12682-x86_64.tar.gz && \
    rm -rf pylon-5.1.0.12682-x86_64.tar.gz && \
    rm -rf pylon-5.1.0.12682-x86_64/pylonSDK-5.1.0.12682-x86_64.tar.gz

# Building the latest pypyplon from source
RUN git clone https://github.com/basler/pypylon.git && \
    cd pypylon && \
    pip3 install .

RUN apt-get install -y vim

ENTRYPOINT ["tail", "-f", "/dev/null"]

HEALTHCHECK NONE
