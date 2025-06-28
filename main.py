import os
import subprocess

from generator.form.form import FormManager
from generator.telegram.telegram import send_pdf, send_turns
from generator.template.template import generate_template


def main():
    form_manager = FormManager()
    form_manager.generate_dat_file()

    ban_names = form_manager.ban_names

    if len(ban_names) == 0:
        print("Gli animatori sono stati bravi e sanno leggere quello che scrivo")
    else:
        print(f"Animatori che non sanno leggere quello che scrivo: {ban_names}")

    turns = generate_template()

    PDF_FILENAME = "turni.pdf"
    TYP_FILENAME = [f for f in os.listdir() if f.endswith("typ")][0]
    subprocess.run(["typst", "compile", TYP_FILENAME, PDF_FILENAME])

    send_pdf(PDF_FILENAME)
    send_turns(turns)


if __name__ == "__main__":
    main()
