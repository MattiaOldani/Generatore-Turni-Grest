import json
import os
import telebot


class TelegramChannel:
    def __init__(self):
        with open("environment.json", "r") as f:
            environment = json.load(f)

        self.telegram_API_key = environment["TELEGRAM_API_KEY"]
        self.channel_ID = environment["CHANNEL_ID"]
        self.bot = telebot.TeleBot(self.telegram_API_key)

    def send_pdf(self, filename):
        with open(filename, "rb") as f:
            caption = "*Turni della settimana*"
            self.bot.send_document(
                self.channel_ID, f, caption=caption, parse_mode="markdown"
            )

    def send_turns(self, turns):
        counts = turns.get_animators_turns_counts(sort=True)
        message = "\n".join(
            ["*Numero di turni per animatore*"]
            + list(map(lambda x: f"{x[0]}: {x[1]}", counts))
        )
        self.bot.send_message(self.channel_ID, message, parse_mode="markdown")

        os.rename("turni_obbligatori.txt", "vecchi_turni_obbligatori.txt")

        no_turns = [name for name, _ in filter(lambda x: x[1] == 0, counts)]
        with open("turni_obbligatori.txt", "w") as f:
            f.write("\n".join(["".join(name.split()) for name in no_turns]) + "\n")
