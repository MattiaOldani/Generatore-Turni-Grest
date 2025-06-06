from functools import cmp_to_key

from utils.days import Days
from utils.slots import Slots


class Turns:
    def __init__(self, data: str) -> None:
        # Parsing
        results = data.split("\n")[4:][::-1][2:][::-1]

        def compare(x, y):
            return x[0].value - y[0].value

        compare = cmp_to_key(compare)

        def format(name):
            results = name[0]
            for char in name[1:]:
                if char.isupper():
                    results += " "
                results += char
            return results

        turns = dict()
        animators = set()
        for slot in Slots:
            availability = list()
            for i, row in enumerate(results):
                if row == "" or row == ";":
                    availability.sort(key=compare)
                    turns[slot.name] = availability
                    results = results[i + 3 :]
                    break
                else:
                    animator = format(row.split(" ")[0])
                    animators.add(animator)
                    keep = list(filter(lambda x: x in ("0", "1"), row.split(" ")))
                    for day in Days:
                        if keep[day.value] == "0":
                            continue
                        availability.append((day, animator))

        counts = dict()
        for i, row in enumerate(results):
            if row == ";":
                results = results[i + 2 :]
                break
            else:
                row = row.strip().split(" ")
                row = list(filter(lambda x: x != "", row))
                for i in range(0, len(row), 2):
                    name = format(row[i])
                    counts[name] = int(row[i + 1])

        max_ = int(results.pop(0).split(" ")[2])
        min_ = int(results.pop(0).split(" ")[2])

        results.pop(0)
        objective = int(results.pop().split(" ")[2])

        # Variabili di istanza
        self.max_ = max_
        self.min_ = min_
        self.animators = animators
        self.counts = counts
        self.objective = objective
        self.turns = turns

    def get_animators(self, slot, day):
        def compare(x, y):
            return x[1] < y[1]

        compare = cmp_to_key(compare)

        return list(
            filter(
                lambda x: x[0].value == day.value,
                sorted(self.turns[slot.name], key=compare),
            )
        )

    def get_animators_turns_counts(self, sort=False, reverse=False):
        counts = list(self.counts.items())
        counts.sort(key=lambda x: x[0])

        match [isinstance(sort, bool), isinstance(reverse, bool)]:
            case [True, True]:
                if sort:
                    counts.sort(key=lambda x: x[1], reverse=reverse)
            case [True, False]:
                raise ValueError("Il parametro 'reverse' deve essere booleano")
            case [False, True]:
                raise ValueError("Il parametro 'sort' deve essere booleano")
            case _:
                ...

        return counts
