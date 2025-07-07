from generator.indexes.days import Days
from generator.indexes.slots import Slots


class TemplateGenerator:
    def __init__(self, solver):
        self.solver = solver

    def generate_template(self):
        days = [day.value for day in Days]
        slots = [slot.value for slot in Slots]

        with open("template.typ", "a") as f:
            for slot in slots:
                f.write(f"\t[{slot}], ")

                for day in days:
                    animators = self.solver.get_slot_assignment(slot, day)
                    names = ", ".join(animators)
                    if names == "":
                        names = "-"
                    f.write(f"[{names}], ")
                f.write("\n")
            f.write(")\n")
