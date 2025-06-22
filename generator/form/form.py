import os
import requests

from dotenv import load_dotenv

from utils.days import Days
from utils.slots import Slots


def generate_dat_file():
    load_dotenv()
    environment = os.environ

    FORM_ENDPOINT = environment["FORM_ENDPOINT"]
    FORM_API_KEY = environment["FORM_API_KEY"]

    headers = {"Authorization": f"Bearer {FORM_API_KEY}"}

    entries = requests.get(FORM_ENDPOINT, headers=headers).json()["submissions"]

    DAYS = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]

    turns = dict()
    names = list()
    for entry in entries:
        entry = entry["responses"]

        surname = "".join(
            [
                s.capitalize()
                for s in entry.pop(1)["answer"].strip().replace("'", "").split()
            ]
        )

        name = surname + "".join(
            [
                n.capitalize()
                for n in entry.pop(0)["answer"].strip().replace("'", "").split()
            ]
        )

        names.append(name)

        pre = [0, 0, 0, 0, 0]
        mensa = [0, 0, 0, 0, 0]
        post = [0, 0, 0, 0, 0]

        for other in entry:
            answers = other["answer"]
            match other["questionId"]:
                case "ApJN0e":
                    for answer in answers:
                        pre[DAYS.index(answer)] = 1
                case "Bp1qgR":
                    for answer in answers:
                        mensa[DAYS.index(answer)] = 1
                case "kGAXpo":
                    for answer in answers:
                        post[DAYS.index(answer)] = 1

        turns[name] = [pre, mensa, post]

    with open("data.dat", "w") as f:
        slots = [f"0{s.value + 1}_{s.name}" for s in Slots]
        f.write(f"set FasceOrarie := {' '.join(slots)};\n\n")

        days = [f"0{day.value + 1}_{day.name}" for day in Days]
        f.write(f"set Giorni := {' '.join(days)};\n\n")

        f.write(f"set Animatori := {' '.join(names)};\n\n")

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

        ANIMATORS_PRE = environment["ANIMATORS_PRE"]
        f.write(f"param AnimatoriPre := {ANIMATORS_PRE};\n\n")

        ANIMATORS_POST = environment["ANIMATORS_POST"]
        f.write(f"param AnimatoriPost := {ANIMATORS_POST};\n\n")

        ANIMATORS_LUNCH = environment["ANIMATORS_LUNCH"]
        f.write(f"param AnimatoriMensa := {ANIMATORS_LUNCH};\n\n")

        ANIMATORS_SHARE_LUNCH = environment["ANIMATORS_SHARE_LUNCH"]
        f.write(f"param AnimatoriPranzoCondiviso := {ANIMATORS_SHARE_LUNCH};\n\n")

        MAX_REPETITION_SAME_SLOT = environment["MAX_REPETITION_SAME_SLOT"]
        f.write(
            f"param MassimaRipetizioneStessoTurno := {MAX_REPETITION_SAME_SLOT};\n\n"
        )

        MAX_NUMBER_DAILY_SLOTS = environment["MAX_NUMBER_DAILY_SLOTS"]
        f.write(f"param MassimoNumeroTurniGiornalieri := {MAX_NUMBER_DAILY_SLOTS};\n")


if __name__ == "__main__":
    ...
