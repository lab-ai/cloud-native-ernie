FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.7 python3.7-dev python3-pip

RUN ln -sfn /usr/bin/python3.7 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python && ln -sfn /usr/bin/pip3 /usr/bin/pip

RUN pip install --upgrade pip
RUN python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
RUN pip install paddle-ernie
RUN pip install --upgrade "jina[devel]"
RUN apt-get install -y libgl1-mesa-dev