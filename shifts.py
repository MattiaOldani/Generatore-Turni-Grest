from functools import cmp_to_key

from days import Days
from turns import Turns


class Shifts():
    
    def __init__(self, data: str):
        # Parsing
        results = data.split("\n")[12:][::-1][2:][::-1]

        def compare(x,y):
            return x[0].value - y[0].value
        compare = cmp_to_key(compare)

        shifts = dict()
        animators = set()
        for turn in Turns:
            turns = list()
            for i,row in enumerate(results):
                if row == "" or row == ";":
                    turns.sort(key=compare)
                    shifts[turn.name] = turns
                    results = results[i+3:]
                    break
                else:
                    animator = row.split(" ")[0]
                    animators.add(animator)
                    keep = list(filter(lambda x : x in ("0","1"), row.split(" ")))
                    for day in Days:
                        if keep[day.value] == "0":
                            continue
                        turns.append((day, animator))
        
        value_counts = dict()
        for i,row in enumerate(results):
            if row == ";":
                results = results[i+2:]
                break
            else:
                row = row.strip().split(" ")
                value_counts[row[0]] = int(row[-1])

        max_ = int(results.pop(0).split(" ")[2])
        min_ = int(results.pop(0).split(" ")[2])

        results.pop(0)
        obj = int(results.pop().split(" ")[2])

        # Variabili di istanza
        self.max_ = max_
        self.min_ = min_
        self.animators = animators
        self.counts = value_counts
        self.obj = obj
        self.shifts = shifts

        print(self.counts)
        print(self.animators)
        print(self.obj)
        print(self.max_, self.min_)
        print(self.shifts)
