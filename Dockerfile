# https://github.com/typst/typst/blob/main/Dockerfile
FROM ghcr.io/typst/typst:latest AS build

FROM ubuntu:latest
COPY --from=build /bin/typst /bin

WORKDIR /application

RUN apt update && apt upgrade -y

RUN apt install python3 python3-venv wget -y

RUN wget https://homes.di.unimi.it/righini/Didattica/ampl_linux-intel64.tgz && \
    tar -zxvf ampl_linux-intel64.tgz && \
    rm ampl_linux-intel64.tgz && \
    mv ampl_linux-intel64 ampl

RUN python3 -m venv venv

ENV PATH $PATH:/application/venv/bin:/application/ampl

COPY generator/ generator/
COPY requirements.txt requirements.txt
COPY start.sh start.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/sh", "start.sh"]
