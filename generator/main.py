import os
import subprocess

from form.form import generate_dat_file
from telegram.telegram import send_pdf, send_turns
from template.template import generate_template


def main():
    generate_dat_file()

    turns = generate_template()

    PDF_FILENAME = "turni.pdf"
    TYP_FILENAME = [f for f in os.listdir() if f.endswith("typ")][0]
    subprocess.run(["typst", "compile", TYP_FILENAME, PDF_FILENAME])

    send_pdf(PDF_FILENAME)
    send_turns(turns)


if __name__ == "__main__":
    main()
