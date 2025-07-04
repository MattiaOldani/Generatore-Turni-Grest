import os
import re
import subprocess

from generator.utils.days import Days
from generator.utils.slots import Slots
from generator.utils.turns import Turns


class TemplateGenerator:
    def __init__(self): ...

    def generate_template(self):
        filename = [f for f in os.listdir() if f.endswith(".mod")][0]

        datafile = [f for f in os.listdir() if f.endswith(".dat")][0]
        variables, objective = self.__parse_file(filename)

        contents = (
            "reset;\n"
            f"model {filename};\n"
            f"data {datafile};\n"
            f"option solver baron;\n"
            "solve;\n"
            f"display {', '.join(variables)};\n"
            f"display {objective};\n"
        )

        runfile = ".".join(filename.split(".")[:-1]) + ".run"
        with open(runfile, "w+") as f:
            f.write(contents)

        results = subprocess.check_output(["ampl", runfile]).decode("utf-8")

        turns = Turns(results)

        with open("template.typ", "a") as f:
            for slot in Slots:
                f.write(f"\t[*{slot.name}*], ")
                for day in Days:
                    animators = turns.get_animators(slot, day)
                    names = ", ".join([a[1] for a in animators])
                    if names == "":
                        names = "-"
                    f.write(f"[{names}], ")
                f.write("\n")
            f.write(")\n")

        self.turns = turns

    def __parse_file(self, filename: str):
        with open(filename, "r+") as f:
            contents = [line.strip() for line in f.readlines()]

        objective = None
        variables = list()
        for line in contents:
            if line.startswith("var"):
                result = re.findall(re.compile(r"(?<=var )(\w+)"), line)
                if result is not None:
                    variables.append(result[0])

            if line.startswith("maximize") or line.startswith("minimize"):
                result = re.findall(
                    re.compile(r"(?<=(?<=maximize )|(?<=minimize ))(\w+)"), line
                )
                if result is not None:
                    objective = result[0]

            if line.startswith("data"):
                break

        return variables, objective
