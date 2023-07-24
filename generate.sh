#!/bin/bash

# Generazione file data.dat
cd script
mv *.py form
cd form

python form.py

# Generazione file turni.pdf
cd ..
mv form/days.py form/slots.py form/data.dat template
cd template
cp template.typ copy.typ

python template.py
typst compile template.typ turni.pdf

# Pulizia post generazione file turni.pdf
rm data.dat turni.run
mv days.py slots.py ../

cp copy.typ template.typ
rm copy.typ

# Invio su telegram
cd ..
mv template/turni.pdf telegram
cd telegram

python telegram.py

# Pulizia post invio su telegram
rm turni.pdf

exit
