import os
import re
import subprocess


def parse_file(filename: str):
    with open(filename, "r+") as f:
        contents = [line.strip() for line in f.readlines()]

    variables = []
    objective = None
    for line in contents:
        if line.startswith("var"):
            if res := re.findall(re.compile(r"(?<=var )(\w+)"), line):
                variables.append(res[0])

        if line.startswith("maximize") or line.startswith("minimize"):
            if res := re.findall(re.compile(r"(?<=(?<=maximize )|(?<=minimize ))(\w+)"), line):
                objective = res[0]

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
    )

    if objective:
        contents += f"display: {objective};\n"

    runfile = ".".join(filename.split(".")[:-1]) + ".run"
    with open(runfile, "w+") as f:
        f.write(contents)

    subprocess.call(["ampl", runfile])

    # Da salvare output ed estrarre i turni


if __name__ == "__main__":
    main()
