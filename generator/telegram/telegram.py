import json
import os
import telebot


with open("environment.json", "r") as f:
    environment = json.load(f)
TELEGRAM_API_KEY = environment["TELEGRAM_API_KEY"]
CHANNEL_ID = environment["CHANNEL_ID"]


def send_pdf(filename):
    bot = telebot.TeleBot(TELEGRAM_API_KEY)

    with open(filename, "rb") as f:
        caption = "*Turni della settimana*"
        bot.send_document(CHANNEL_ID, f, caption=caption, parse_mode="markdown")


def send_turns(turns):
    bot = telebot.TeleBot(TELEGRAM_API_KEY)

    counts = turns.get_animators_turns_counts(sort=True)
    message = "\n".join(
        ["*Numero di turni per animatore*"]
        + list(map(lambda x: f"{x[0]}: {x[1]}", counts))
    )
    bot.send_message(CHANNEL_ID, message, parse_mode="markdown")

    os.rename("turni_obbligatori.txt", "vecchi_turni_obbligatori.txt")

    no_turns = [name for name, _ in filter(lambda x: x[1] == 0, counts)]
    with open("turni_obbligatori.txt", "w") as f:
        f.write("\n".join(["".join(name.split()) for name in no_turns]) + "\n")


if __name__ == "__main__":
    ...
