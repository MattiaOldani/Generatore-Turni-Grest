import json
import requests

from thefuzz import fuzz

from generator.utils.days import Days
from generator.utils.slots import Slots


class FormManager:
    DAYS_INDEX = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"]

    SURNAME_ID = "WRpKWk"
    NAME_ID = "erx0Jl"

    # Indici che non servono, ma che mi salvo per sicurezza
    # ARCO_ETA = "xDNloy"
    # PISCINA = "xDNLgo"
    # GITA = "P9BWLd"

    def __init__(self):
        with open("environment.json", "r") as f:
            environment = json.load(f)

        self.form_endpoint = environment["FORM_ENDPOINT"]
        self.form_API_key = environment["FORM_API_KEY"]
        self.pre = environment["ANIMATORS_PRE"]
        self.lunch = environment["ANIMATORS_LUNCH"]
        self.post = environment["ANIMATORS_POST"]
        self.share_lunch = environment["ANIMATORS_SHARE_LUNCH"]
        self.max_repetition_same_slot = environment["MAX_REPETITION_SAME_SLOT"]
        self.max_number_daily_slots = environment["MAX_NUMBER_DAILY_SLOTS"]

    def generate_dat_file(self):
        headers = {"Authorization": f"Bearer {self.form_API_key}"}

        entries = requests.get(self.form_endpoint, headers=headers).json()[
            "submissions"
        ]

        animators_pre = [0, 0, 0, 0, 0]
        animators_post = [0, 0, 0, 0, 0]
        animators_lunch = [0, 0, 0, 0, 0]

        turns = dict()
        must_turns = dict()
        names = list()
        need_names = dict()

        for entry in entries:
            entry = entry["responses"]

            surname_index = 0
            for i, answer in enumerate(entry):
                if answer["questionId"] == FormManager.SURNAME_ID:
                    surname_index = i
                    break

            surname = entry.pop(surname_index)["answer"].strip()
            while "  " in surname:
                surname = surname.replace("  ", " ")

            surname = "".join(
                s.strip().replace("(", "").replace(")", "").capitalize()
                for s in surname.split()
            )

            name_index = 0
            for i, answer in enumerate(entry):
                if answer["questionId"] == FormManager.NAME_ID:
                    name_index = i
                    break

            name = entry.pop(name_index)["answer"].strip()
            while "  " in name:
                name = name.replace("  ", " ")

            name = surname + "".join(
                s.strip().replace("(", "").replace(")", "").capitalize()
                for s in name.split()
            )

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
                    case "bevODZ":
                        must_flag = 1
                        for answer in answers:
                            must_pre[FormManager.DAYS_INDEX.index(answer)] = 1
                            animators_pre[FormManager.DAYS_INDEX.index(answer)] += 1
                    case "Apy80z":
                        must_flag = 1
                        for answer in answers:
                            must_mensa[FormManager.DAYS_INDEX.index(answer)] = 1
                            animators_lunch[FormManager.DAYS_INDEX.index(answer)] += 1
                    case "Bp0BgK":
                        must_flag = 1
                        for answer in answers:
                            must_post[FormManager.DAYS_INDEX.index(answer)] = 1
                            animators_post[FormManager.DAYS_INDEX.index(answer)] += 1
                    case "kGvZpe":
                        for answer in answers:
                            pre[FormManager.DAYS_INDEX.index(answer)] = 1
                    case "vDK2pD":
                        for answer in answers:
                            mensa[FormManager.DAYS_INDEX.index(answer)] = 1
                    case "Kxk0gV":
                        for answer in answers:
                            post[FormManager.DAYS_INDEX.index(answer)] = 1

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
            animators_pre[i] = max(animators_pre[i], self.pre)
            animators_post[i] = max(animators_post[i], self.post)
            animators_lunch[i] = max(animators_lunch[i], self.lunch)

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
                result += f"{days[day.value]} {animators_pre[i]}\n"
                if day.value == 4:
                    result = result.strip() + ";\n\n"
            f.write(result)

            f.write("param AnimatoriPost :=\n")

            result = str()
            for i, day in enumerate(Days):
                result += f"{days[day.value]} {animators_post[i]}\n"
                if day.value == 4:
                    result = result.strip() + ";\n\n"
            f.write(result)

            f.write("param AnimatoriMensa :=\n")

            result = str()
            for i, day in enumerate(Days):
                result += f"{days[day.value]} {animators_lunch[i]}\n"
                if day.value == 4:
                    result = result.strip() + ";\n\n"
            f.write(result)

            f.write(f"param AnimatoriPranzoCondiviso := {self.share_lunch};\n\n")

            f.write(
                f"param MassimaRipetizioneStessoTurno := {self.max_repetition_same_slot};\n\n"
            )

            f.write(
                f"param MassimoNumeroTurniGiornalieri := {self.max_number_daily_slots};\n"
            )
