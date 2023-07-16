#!/bin/bash

cp template.md copy.md

python main.py
pandoc -o turni.pdf template.md --pdf-engine=weasyprint

cp copy.md template.md
rm copy.md

exit
