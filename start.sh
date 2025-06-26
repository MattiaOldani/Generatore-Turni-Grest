#!/bin/bash

# Generazione file turni.pdf e invio su telegram
cp template.typ template_copy.typ
cp turni.mod turni_copy.mod

python main.py

# Pulizia post invio su telegram
cp template_copy.typ template.typ
cp turni_copy.mod turni.mod
rm data.dat template_copy.typ turni_copy.mod turni.run turni.pdf

exit
