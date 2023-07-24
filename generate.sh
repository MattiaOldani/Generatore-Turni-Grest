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

# Configurazione iniziale
rm data.dat turni.run
mv days.py slots.py ../

cp copy.typ template.typ
rm copy.typ

# Da aggiungere spostamento nella cartella per invio su telegram

exit
