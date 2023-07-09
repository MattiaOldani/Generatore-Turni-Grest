#!/bin/bash

fin=$1
fout="${fin%.*}.out"
fsens="${fin%.*}.sens"

glpsol --cover --clique --gomory --mir -m "$fin" -o "$fout" --ranges "$fsens"
