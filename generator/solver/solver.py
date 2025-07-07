import os
import requests

from ortools.sat.python import cp_model
from thefuzz import fuzz

from generator.environment import (
    FORM_API_KEY,
    FORM_ENDPOINT,
    PRE_ANIMATORS,
    POST_ANIMATORS,
    LUNCH_ANIMATORS,
    SHARE_LUNCH_ANIMATORS,
    MAX_REPETITION_SAME_SLOT,
    MAX_NUMBER_DAILY_SLOTS,
)
from generator.indexes.days import Days
from generator.indexes.slots import Slots


class Solver:
    def __init__(self):
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def populate_model(self):
        NAME_ID = "erx0Jl"
        SURNAME_ID = "WRpKWk"

        headers = {"Authorization": f"Bearer {FORM_API_KEY}"}
        entries = requests.get(FORM_ENDPOINT, headers=headers).json()["submissions"]

        availability = {}
        necessity = {}
        has_necessity = {}

        days = [day.value for day in Days]
        slots = [slot.value for slot in Slots]
        animators = []

        assignment = {}

        pre_counter = [0, 0, 0, 0, 0]
        lunch_counter = [0, 0, 0, 0, 0]
        post_counter = [0, 0, 0, 0, 0]
        must_pre_counter = [0, 0, 0, 0, 0]
        must_lunch_counter = [0, 0, 0, 0, 0]
        must_post_counter = [0, 0, 0, 0, 0]

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

            surname = "".join(
                s.strip().replace("(", "").replace(")", "").capitalize()
                for s in surname.split()
            )

            name_index = 0
            for i, answer in enumerate(entry):
                if answer["questionId"] == NAME_ID:
                    name_index = i
                    break

            name = entry.pop(name_index)["answer"].strip()
            while "  " in name:
                name = name.replace("  ", " ")

            name = surname + "".join(
                s.strip().replace("(", "").replace(")", "").capitalize()
                for s in name.split()
            )

            animators.append(name)

            for d in days:
                for s in slots:
                    availability[d, name, s] = 0
                    necessity[d, name, s] = 0

            must_flag = 0
            for answers in entry:
                question_ID = answers["questionId"]
                answers = answers["answer"]

                if len(answers) == 0:
                    continue

                match question_ID:
                    case "bevODZ":
                        must_flag = 1
                        for answer in answers:
                            necessity[answer, name, slots[0]] = 1
                            must_pre_counter[days.index(answer)] += 1
                            pre_counter[days.index(answer)] += 1
                    case "Apy80z":
                        must_flag = 1
                        for answer in answers:
                            necessity[answer, name, slots[1]] = 1
                            must_lunch_counter[days.index(answer)] += 1
                            lunch_counter[days.index(answer)] += 1
                    case "Bp0BgK":
                        must_flag = 1
                        for answer in answers:
                            necessity[answer, name, slots[2]] = 1
                            must_post_counter[days.index(answer)] += 1
                            post_counter[days.index(answer)] += 1
                    case "kGvZpe":
                        for answer in answers:
                            availability[answer, name, slots[0]] = 1
                            pre_counter[days.index(answer)] += 1
                    case "vDK2pD":
                        for answer in answers:
                            availability[answer, name, slots[1]] = 1
                            lunch_counter[days.index(answer)] += 1
                    case "Kxk0gV":
                        for answer in answers:
                            availability[answer, name, slots[2]] = 1
                            post_counter[days.index(answer)] += 1

                has_necessity[name] = must_flag

        for d in days:
            for a in animators:
                for s in slots:
                    assignment[d, a, s] = self.model.NewBoolVar(
                        f"assignment_{d}_{a}_{s}"
                    )

        with open("turni_obbligatori.txt", "r") as f:
            must_do_something = [line.strip() for line in f.readlines()]

        if len(must_do_something) > 0:
            os.rename("turni_obbligatori.txt", "vecchi_turni_obbligatori.txt")

        for i, name in enumerate(must_do_something):
            if name not in animators:
                max_ratio = 0
                max_name = ""
                for other in animators:
                    current_ratio = fuzz.ratio(name, other)
                    if current_ratio > max_ratio:
                        max_ratio = current_ratio
                        max_name = other

                print(f"Animatore {name} cambiato in {max_name}")
                must_do_something[i] = max_name

                for d in days:
                    for s in slots:
                        assignment[d, max_name, s] = self.model.NewBoolVar(
                            f"assignment_{d}_{max_name}_{s}"
                        )

                # vincolo turni obbligatori
                self.model.Add(
                    sum(assignment[d, max_name, s] for d in days for s in slots) >= 1
                )

        pre_animators = {}
        lunch_animators = {}
        post_animators = {}

        for i, day in enumerate(days):
            if pre_counter[i] == 0:
                pre_animators[day] = 0
            else:
                pre_animators[day] = max(must_pre_counter[i], PRE_ANIMATORS)

            if lunch_counter[i] == 0:
                lunch_animators[day] = 0
            else:
                if i == 3:
                    lunch_animators[day] = max(
                        must_lunch_counter[i], SHARE_LUNCH_ANIMATORS
                    )
                else:
                    lunch_animators[day] = max(must_lunch_counter[i], LUNCH_ANIMATORS)

            if post_counter[i] == 0:
                post_animators[day] = 0
            else:
                post_animators[day] = max(must_post_counter[i], POST_ANIMATORS)

        turns_number = {
            a: self.model.NewIntVar(0, 15, f"turns_number_{a}") for a in animators
        }

        must_turns_number = {
            a: self.model.NewIntVar(0, 15, f"must_turns_number_{a}") for a in animators
        }

        max_turns_number = self.model.NewIntVar(0, 15, "max_turns_number")

        min_turns_number = self.model.NewIntVar(0, 15, "min_turns_number")

        # vincolo necessità
        for a in animators:
            if has_necessity[a] == 0:
                continue

            for d in days:
                for s in slots:
                    self.model.Add(assignment[d, a, s] == necessity[d, a, s])

        # vincolo animatori pre
        for d in days:
            self.model.Add(
                sum(assignment[d, a, slots[0]] for a in animators) == pre_animators[d]
            )

        # vincolo animatori mensa
        for d in days:
            self.model.Add(
                sum(assignment[d, a, slots[1]] for a in animators) == lunch_animators[d]
            )

        # vincolo animatori post
        for d in days:
            self.model.Add(
                sum(assignment[d, a, slots[2]] for a in animators) == post_animators[d]
            )

        # vincolo numero turni
        for a in animators:
            self.model.Add(
                turns_number[a] == sum(assignment[d, a, s] for d in days for s in slots)
            )

        # vincolo massimo numero turni
        for a in animators:
            self.model.Add(max_turns_number >= (1 - has_necessity[a]) * turns_number[a])

        # vincolo minimo numero turni
        for a in animators:
            self.model.Add(min_turns_number <= turns_number[a])

        # vincolo turni necessità
        for a in animators:
            self.model.Add(
                must_turns_number[a]
                == has_necessity[a]
                * (
                    sum(assignment[d, a, s] for d in days for s in slots)
                    - sum(necessity[d, a, s] for d in days for s in slots)
                )
            )

        # vincolo zero turni necessità
        self.model.Add(sum(must_turns_number[a] for a in animators) == 0)

        # vincolo turno solo se disponibile
        for d in days:
            for a in animators:
                for s in slots:
                    self.model.Add(
                        assignment[d, a, s]
                        <= availability[d, a, s] + necessity[d, a, s]
                    )

        # vincolo stesso turno
        for a in animators:
            if has_necessity[a] == 1:
                continue

            for s in slots:
                self.model.Add(
                    sum(assignment[d, a, s] for d in days) <= MAX_REPETITION_SAME_SLOT
                )

        # vincolo più turni stesso giorno
        for a in animators:
            if has_necessity[a] == 1:
                continue

            for d in days:
                self.model.Add(
                    sum(assignment[d, a, s] for s in slots) <= MAX_NUMBER_DAILY_SLOTS
                )

        # funzione obiettivo
        self.model.Minimize(max_turns_number - min_turns_number)

        self.animators = sorted(animators)
        self.turns_number = turns_number
        self.assignment = assignment

    def solve(self):
        status = self.solver.Solve(self.model)

        self.turns_number = sorted(
            [(a, self.solver.Value(self.turns_number[a])) for a in self.animators],
            key=lambda x: x[1],
            reverse=True,
        )

        if status == cp_model.OPTIMAL:
            return 0
        else:
            return 1

    def get_slot_assignment(self, slot, day):
        animators = []
        for a in self.animators:
            if self.solver.Value(self.assignment[day, a, slot]):
                animators += [a]

        return animators

    def get_turns_number(self):
        return self.turns_number
