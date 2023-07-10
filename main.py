import os
import re
import subprocess

from shifts import Shifts


def parse_file(filename: str):
    with open(filename, "r+") as f:
        contents = [line.strip() for line in f.readlines()]

    variables = []
    objective = None
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
    )

    if objective:
        contents += f"display: {objective};\n"

    runfile = ".".join(filename.split(".")[:-1]) + ".run"
    with open(runfile, "w+") as f:
        f.write(contents)

    results = subprocess.check_output(["ampl", runfile]).decode("utf-8")
    results = results.split("\n")[10:][::-1][2:][::-1]

    shifts = dict()
    LABELS = ["PRE", "MENSA", "POST"]
    for t in range(3):
        rows = list()
        for i,row in enumerate(results):
            if row == "" or row == ";":
                shifts[LABELS[t]] = '\n'.join(rows[2:])
                jump = i+1 if row == "" else i+2
                results = results[jump:]
                break
            else:
                rows.append(row)
    
    shifts_value_counts = list()
    for i,row in enumerate(results):
        if row == ";":
            shifts_value_counts = '\n'.join(shifts_value_counts[1:])
            results = results[i+2:]
            break
        else:
            shifts_value_counts.append(row)

    number_of_shifts = '\n'.join(results[:2])
    results = results[3:]

    objective = results.pop()

    result = Shifts(shifts, shifts_value_counts, number_of_shifts, objective)

    print(result)


if __name__ == "__main__":
    main()
