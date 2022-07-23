FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y debhelper \
    python3 \
    python3-pip \
    python3-flask

RUN pip3 install -U pyinstaller \
    psutil