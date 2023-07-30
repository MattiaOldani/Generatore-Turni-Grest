#!/bin/bash

docker build -t mattiaoldani/generatore .
docker run mattiaoldani/generatore:latest

exit
