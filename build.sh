#!/bin/bash

docker build -t mattiaoldani/generatore .
docker push mattiaoldani/generatore:latest

exit
