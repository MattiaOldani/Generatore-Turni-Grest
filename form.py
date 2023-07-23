import base64
import requests

from days import Days
from environment import FORM_API_KEY, ENDPOINT
from turns import Turns


def main():
    authcode = base64.b64encode(f"{FORM_API_KEY}:ciao".encode()).decode()
    headers = {"Authorization" : f"Basic {authcode}"}

    entries = requests.get(ENDPOINT, headers=headers).json()["Entries"]

    PRE = ["Field105", "Field106", "Field107", "Field108", "Field109"]
    MENSA = ["Field305", "Field306", "Field307", "Field308", "Field309"]
    POST = ["Field205", "Field206", "Field207", "Field208", "Field209"]

    turns = dict()
    names = list()
    for entry in entries:
        name = entry["Field1"].strip() + entry["Field2"].strip()
        names.append(name)
        
        pre = list()
        for field in PRE:
            if entry[field] == "":
                pre.append("0")
            else:
                pre.append("1")
        
        mensa = list()
        for field in MENSA:
            if entry[field] == "":
                mensa.append("0")
            else:
                mensa.append("1")

        post = list()
        for field in POST:
            if entry[field] == "":
                post.append("0")
            else:
                post.append("1")
        
        turns[name] = [pre, mensa, post] 

    with open("data.dat", "w") as f:
        shifts = [f"0{t.value+1}_{t.name}" for t in Turns]
        
        f.write(f"set FasceOrarie := {' '.join(shifts)};\n\n")
        days = [f"0{day.value+1}_{day.name}" for day in Days]
        
        f.write(f"set Giorni := {' '.join(days)};\n\n")
        f.write(f"set Animatori := {' '.join(names)};\n\n")
        
        f.write(f"param Disponibilita: {' '.join(shifts)} :=\n")

        for day in Days:
            result = str()
            for name in names:
                result = result + days[day.value] + " " + name + " "
                t = turns[name]
                toto = t[0][day.value] + " " + t[1][day.value] + " " + t[2][day.value]
                result += toto + "\n"
            if day.value == 4:
                result = result.strip() + ";\n"
            f.write(result)


if __name__ == "__main__":
    main()
