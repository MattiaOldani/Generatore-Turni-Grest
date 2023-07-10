class Shifts():
    def __init__(self, shifts: dict, counts: str, max_min_shifts: str, obj: str):
        self.shifts = '\n\n'.join(shifts.values())
        self.counts = counts
        self.max_min_shifts = max_min_shifts
        self.obj = obj

    def __str__(self):
        return f"{self.shifts}\n\n{self.counts}\n\n{self.max_min_shifts}\n\n{self.obj}"
