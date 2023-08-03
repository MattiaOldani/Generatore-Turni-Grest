# https://github.com/typst/typst/blob/main/Dockerfile
FROM rust:alpine AS build
COPY typst /app
WORKDIR /app
ENV CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse
RUN apk add --update musl-dev && cargo build -p typst-cli --release

# ampl e python
FROM ubuntu:latest
COPY --from=build /app/target/release/typst /bin

WORKDIR /application

RUN apt update && apt upgrade -y

RUN apt install wget -y
RUN wget https://homes.di.unimi.it/righini/Didattica/ampl_linux-intel64.tgz
RUN tar -zxvf ampl_linux-intel64.tgz
RUN rm ampl_linux-intel64.tgz
RUN mv ampl_linux-intel64 ampl
ENV PATH $PATH:/application/ampl

RUN apt install python3 python3-venv -y
RUN python3 -m venv .
ENV PATH $PATH:/application/bin

COPY generator/ generator/
COPY generate.sh generate.sh
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/sh", "generate.sh"]
