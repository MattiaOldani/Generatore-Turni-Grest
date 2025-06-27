import json
import requests

from thefuzz import fuzz

from generator.utils.days import Days
from generator.utils.slots import Slots


def generate_dat_file():
    with open("environment.json", "r") as f:
        environment = json.load(f)

    FORM_ENDPOINT = environment["FORM_ENDPOINT"]
    FORM_API_KEY = environment["FORM_API_KEY"]

    headers = {"Authorization": f"Bearer {FORM_API_KEY}"}

    entries = requests.get(FORM_ENDPOINT, headers=headers).json()["submissions"]

    PRE_POST_INDEX = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]

    LUNCH_INDEX = [
        "Lunedì",
        "Martedì",
        "Mercoledì",
        "Giovedì [pranzo condiviso]",
        "Venerdì",
    ]

    SURNAME_ID = "bekXD1"
    NAME_ID = "7KDOe0"

    ANIMATORS_PRE = [0, 0, 0, 0, 0]
    ANIMATORS_POST = [0, 0, 0, 0, 0]
    ANIMATORS_LUNCH = [0, 0, 0, 0, 0]

    turns = dict()
    must_turns = dict()
    names = list()
    ban_names = set()
    need_names = dict()
    for entry in entries:
        entry = entry["responses"]

        surname_index = 0
        for i, answer in enumerate(entry):
            if answer["questionId"] == SURNAME_ID:
                surname_index = i
                break

        surname = entry.pop(surname_index)["answer"].strip()
        while "  " in surname:
            surname = surname.replace("  ", " ")

        surname = "".join(s.strip().capitalize() for s in surname.split())

        name_index = 0
        for i, answer in enumerate(entry):
            if answer["questionId"] == NAME_ID:
                name_index = i
                break

        name = entry.pop(name_index)["answer"].strip()
        while "  " in name:
            name = name.replace("  ", " ")

        name = surname + "".join(s.strip().capitalize() for s in name.split())

        names.append(name)

        pre = [0, 0, 0, 0, 0]
        mensa = [0, 0, 0, 0, 0]
        post = [0, 0, 0, 0, 0]

        must_pre = [0, 0, 0, 0, 0]
        must_mensa = [0, 0, 0, 0, 0]
        must_post = [0, 0, 0, 0, 0]

        must_flag = 0
        for other in entry:
            answers = other["answer"]

            if len(answers) == 0:
                continue

            match other["questionId"]:
                case "ApJN0e":
                    must_flag = 1
                    for answer in answers:
                        must_pre[PRE_POST_INDEX.index(answer)] = 1
                        ANIMATORS_PRE[PRE_POST_INDEX.index(answer)] += 1
                case "Bp1qgR":
                    must_flag = 1
                    for answer in answers:
                        must_mensa[LUNCH_INDEX.index(answer)] = 1
                        ANIMATORS_LUNCH[LUNCH_INDEX.index(answer)] += 1
                case "kGAXpo":
                    must_flag = 1
                    for answer in answers:
                        must_post[PRE_POST_INDEX.index(answer)] = 1
                        ANIMATORS_POST[PRE_POST_INDEX.index(answer)] += 1
                case "rOEjxN":
                    for answer in answers:
                        pre[PRE_POST_INDEX.index(answer)] = 1
                case "47j4WX":
                    for answer in answers:
                        mensa[LUNCH_INDEX.index(answer)] = 1
                case "joxada":
                    for answer in answers:
                        post[PRE_POST_INDEX.index(answer)] = 1

        for i in range(len(pre)):
            if must_pre[i] == 1:
                if pre[i] == 1:
                    ban_names.add(name)
                pre[i] = 0
            if must_mensa[i] == 1:
                if mensa[i] == 1:
                    ban_names.add(name)
                mensa[i] = 0
            if must_post[i] == 1:
                if post[i] == 1:
                    ban_names.add(name)
                post[i] = 0

        turns[name] = [pre, mensa, post]
        must_turns[name] = [must_pre, must_mensa, must_post]
        need_names[name] = must_flag

    with open("turni_obbligatori.txt", "r") as f:
        must_do_something = [line.strip() for line in f.readlines()]

    for i, name in enumerate(must_do_something):
        if name not in names:
            max_ratio = 0
            max_name = ""
            for other in names:
                current_ratio = fuzz.ratio(name, other)
                if current_ratio > max_ratio:
                    max_ratio = current_ratio
                    max_name = other

            print(f"Animatore {name} cambiato in {max_name}")
            must_do_something[i] = max_name

    for i in range(5):
        ANIMATORS_PRE[i] = max(ANIMATORS_PRE[i], environment["ANIMATORS_PRE"])
        ANIMATORS_POST[i] = max(ANIMATORS_POST[i], environment["ANIMATORS_POST"])
        ANIMATORS_LUNCH[i] = max(ANIMATORS_LUNCH[i], environment["ANIMATORS_LUNCH"])

    with open("turni.mod", "r") as f:
        model = f.read()

    FORMAT_MODEL = {
        0: ["", "", "", ""],
        1: [
            "# Insieme degli animatori che devono fare per forza un turno",
            "set AnimatoriConTurnoObbligatorio;",
            "# Alcuni animatori devono fare per forza un turno",
            "subject to LevaObbligatoria {a in AnimatoriConTurnoObbligatorio}:\n\tsum {g in Giorni, fo in FasceOrarie} Assegnamento[g,a,fo] >= 1;",
        ],
    }

    INDEX = 0 if len(must_do_something) == 0 else 1
    while "{{}}" in model:
        model = model.replace("{{}}", FORMAT_MODEL[INDEX].pop(0), count=1)

    with open("turni.mod", "w") as f:
        f.write(model)

    with open("data.dat", "w") as f:
        slots = [f"0{s.value + 1}_{s.name}" for s in Slots]
        f.write(f"set FasceOrarie := {' '.join(slots)};\n\n")

        days = [f"0{day.value + 1}_{day.name}" for day in Days]
        f.write(f"set Giorni := {' '.join(days)};\n\n")

        f.write(f"set Animatori := {' '.join(names)};\n\n")

        if len(must_do_something) > 0:
            f.write(
                f"set AnimatoriConTurnoObbligatorio := {' '.join(must_do_something)};\n\n"
            )

        f.write(f"param Disponibilita: {' '.join(slots)} :=\n")

        for day in Days:
            result = str()
            for name in names:
                result = f"{result}{days[day.value]} {name} "
                turn = turns[name]
                turn = f"{turn[0][day.value]} {turn[1][day.value]} {turn[2][day.value]}"
                result = f"{result}{turn}\n"
            if day.value == 4:
                result = result.strip() + ";\n\n"
            f.write(result)

        f.write(f"param Necessita: {' '.join(slots)} :=\n")

        for day in Days:
            result = str()
            for name in names:
                result = f"{result}{days[day.value]} {name} "
                must_turn = must_turns[name]
                must_turn = f"{must_turn[0][day.value]} {must_turn[1][day.value]} {must_turn[2][day.value]}"
                result = f"{result}{must_turn}\n"
            if day.value == 4:
                result = result.strip() + ";\n\n"
            f.write(result)

        f.write("param HannoNecessita :=\n")

        for name in names:
            f.write(f"{name} {need_names[name]}\n")
        f.write(";\n\n")

        f.write("param AnimatoriPre :=\n")

        result = str()
        for i, day in enumerate(Days):
            result += f"{days[day.value]} {ANIMATORS_PRE[i]}\n"
            if day.value == 4:
                result = result.strip() + ";\n\n"
        f.write(result)

        f.write("param AnimatoriPost :=\n")

        result = str()
        for i, day in enumerate(Days):
            result += f"{days[day.value]} {ANIMATORS_POST[i]}\n"
            if day.value == 4:
                result = result.strip() + ";\n\n"
        f.write(result)

        f.write("param AnimatoriMensa :=\n")

        result = str()
        for i, day in enumerate(Days):
            result += f"{days[day.value]} {ANIMATORS_LUNCH[i]}\n"
            if day.value == 4:
                result = result.strip() + ";\n\n"
        f.write(result)

        ANIMATORS_SHARE_LUNCH = environment["ANIMATORS_SHARE_LUNCH"]
        f.write(f"param AnimatoriPranzoCondiviso := {ANIMATORS_SHARE_LUNCH};\n\n")

        MAX_REPETITION_SAME_SLOT = environment["MAX_REPETITION_SAME_SLOT"]
        f.write(
            f"param MassimaRipetizioneStessoTurno := {MAX_REPETITION_SAME_SLOT};\n\n"
        )

        MAX_NUMBER_DAILY_SLOTS = environment["MAX_NUMBER_DAILY_SLOTS"]
        f.write(f"param MassimoNumeroTurniGiornalieri := {MAX_NUMBER_DAILY_SLOTS};\n")

    return ban_names if len(ban_names) > 0 else None


if __name__ == "__main__":
    ...
