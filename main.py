import os
import subprocess

from generator.solver.solver import Solver
from generator.telegram.telegram import TelegramChannel
from generator.template.template import TemplateGenerator


def main():
    solver = Solver()
    solver.populate_model()
    solver.solve()

    template_generator = TemplateGenerator(solver)
    template_generator.generate_template()
    turns = solver.get_turns_number()

    PDF_FILENAME = "turni.pdf"
    TYP_FILENAME = [f for f in os.listdir() if f.endswith("typ")][0]
    subprocess.run(["typst", "compile", TYP_FILENAME, PDF_FILENAME])

    telegram_channel = TelegramChannel()
    telegram_channel.send_pdf(PDF_FILENAME)
    telegram_channel.send_turns(turns)


if __name__ == "__main__":
    main()
