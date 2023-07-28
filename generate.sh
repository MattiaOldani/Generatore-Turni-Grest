#!/bin/bash

# Generazione file turni.pdf e invio su telegram
cd script
cp template.typ template_copy.typ

python main.py

# Pulizia post invio su telegram
cp template_copy.typ template.typ
rm data.dat template_copy.typ turni.run turni.pdf

exit
