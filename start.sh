#!/bin/bash

cp template.typ template_copy.typ

python main.py

cp template_copy.typ template.typ
rm template_copy.typ turni.pdf

exit
