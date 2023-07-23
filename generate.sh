#!/bin/bash

# Generazione file data.dat
python form.py

# Generazione file turni.pdf
cp template.typ copy.typ

python main.py
typst compile template.typ turni.pdf

# Pulizia finale
cp copy.typ template.typ
rm copy.typ

exit
