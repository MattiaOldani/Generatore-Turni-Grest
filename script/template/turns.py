from functools import cmp_to_key

from days import Days
from slots import Slots


class Turns():
    def __init__(self, data: str) -> None:
        # Parsing
        results = data.split("\n")[4:][::-1][2:][::-1]

        def compare(x,y):
            return x[0].value - y[0].value
        compare = cmp_to_key(compare)

        turns = dict()
        animators = set()
        for slot in Slots:
            availability = list()
            for i,row in enumerate(results):
                if row == "" or row == ";":
                    availability.sort(key=compare)
                    turns[slot.name] = availability
                    results = results[i+3:]
                    break
                else:
                    animator = row.split(" ")[0]
                    animators.add(animator)
                    keep = list(filter(lambda x : x in ("0","1"), row.split(" ")))
                    for day in Days:
                        if keep[day.value] == "0":
                            continue
                        availability.append((day, animator))
        
        counts = dict()
        for i,row in enumerate(results):
            if row == ";":
                results = results[i+2:]
                break
            else:
                row = row.strip().split(" ")
                row = list(filter(lambda x : x != "", row))
                for i in range(0,len(row),2):
                    counts[row[i]] = int(row[i+1])

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

    
    def get_animators(self, slot: Slots, day: Days) -> list[tuple[str]]:
        return list(filter(
            lambda x : x[0].value == day.value,
            self.turns[slot.name]
        ))
