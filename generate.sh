#!/bin/bash

# Generazione file data.dat
python form.py

# Generazione file turni.pdf
cp template.md copy.md

python main.py
pandoc -o turni.pdf template.md --pdf-engine=weasyprint

# Pulizia finale
cp copy.md template.md
rm copy.md

exit
