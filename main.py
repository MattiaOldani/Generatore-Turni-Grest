import os
import subprocess

from generator.form.form import FormManager
from generator.telegram.telegram import TelegramChannel
from generator.template.template import TemplateGenerator


def main():
    form_manager = FormManager()
    form_manager.generate_dat_file()

    ban_names = form_manager.ban_names

    if len(ban_names) == 0:
        print("Gli animatori sono stati bravi e sanno leggere quello che scrivo")
    else:
        print(f"Animatori che non sanno leggere quello che scrivo: {ban_names}")

    template_generator = TemplateGenerator()
    template_generator.generate_template()

    turns = template_generator.turns

    PDF_FILENAME = "turni.pdf"
    TYP_FILENAME = [f for f in os.listdir() if f.endswith("typ")][0]
    subprocess.run(["typst", "compile", TYP_FILENAME, PDF_FILENAME])

    telegram_channel = TelegramChannel()
    telegram_channel.send_pdf(PDF_FILENAME)
    telegram_channel.send_turns(turns)


if __name__ == "__main__":
    main()
