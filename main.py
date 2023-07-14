import os
import re
import subprocess

from shifts import Shifts


def parse_file(filename: str):
    with open(filename, "r+") as f:
        contents = [line.strip() for line in f.readlines()]

    objective = None
    variables = list()
    for line in contents:
        if line.startswith("var"):
            result = re.findall(
                re.compile(r"(?<=var )(\w+)"), line
            )
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


def main():
    filename = [f for f in os.listdir() if f.endswith(".mod")][0]
    variables, objective = parse_file(filename)

    contents = (
        "reset;\n"
        f"model {filename};\n"
        f"option solver knitro;\n"
        "solve;\n"
        f"display {', '.join(variables)};\n"
        f"display {objective};\n"
    )

    runfile = ".".join(filename.split(".")[:-1]) + ".run"
    with open(runfile, "w+") as f:
        f.write(contents)

    results = subprocess.check_output(["ampl", runfile]).decode("utf-8")

    shifts = Shifts(results)

    # print(shifts)


if __name__ == "__main__":
    main()
