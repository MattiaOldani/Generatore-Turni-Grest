import base64
import requests

from days import Days
from environment import FORM_API_KEY, ENDPOINT
from slots import Slots


def main():
    authcode = base64.b64encode(f"{FORM_API_KEY}:ciao".encode()).decode()
    headers = {"Authorization" : f"Basic {authcode}"}

    entries = requests.get(ENDPOINT, headers=headers).json()["Entries"]

    PRE = ["Field105", "Field106", "Field107", "Field108", "Field109"]
    MENSA = ["Field305", "Field306", "Field307", "Field309"]
    POST = ["Field205", "Field206", "Field207", "Field208", "Field209"]

    turns = dict()
    names = list()
    for entry in entries:
        name = entry["Field1"].strip() + ''.join(entry["Field2"].strip().split(" "))
        names.append(name)
        
        pre = list()
        for field in PRE:
            pre.append("0" if entry[field] == "" else "1")
        
        mensa = list()
        for field in MENSA:
            mensa.append("0" if entry[field] == "" else "1")
        mensa.insert(3,'0')

        post = list()
        for field in POST:
            post.append("0" if entry[field] == "" else "1")
        
        turns[name] = [pre, mensa, post] 

    with open("data.dat", "w") as f:
        slots = [f"0{s.value+1}_{s.name}" for s in Slots]
        f.write(f"set FasceOrarie := {' '.join(slots)};\n\n")
        
        days = [f"0{day.value+1}_{day.name}" for day in Days]
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
                result = result.strip() + ";\n"
            f.write(result)


if __name__ == "__main__":
    main()
