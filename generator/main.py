import os
import subprocess
import sys

from form.form import generate_dat_file
from telegram.telegram import send_pdf, send_turns
from template.template import generate_template


def main():
    argv = sys.argv[1:]
    animators_per_slot = int(argv[0])
    max_repetition_same_slot = int(argv[1])
    max_number_daily_slots = int(argv[2])

    generate_dat_file(
        animators_per_slot,
        max_repetition_same_slot,
        max_number_daily_slots
    )

    turns = generate_template()

    PDF_FILENAME = "turni.pdf"
    TYP_FILENAME = [f for f in os.listdir() if f.endswith("typ")][0]
    subprocess.run(["typst", "compile", TYP_FILENAME, PDF_FILENAME])

    send_pdf(PDF_FILENAME)
    send_turns(turns)


if __name__ == "__main__":
    main()
