import telebot

from generator.environment import TELEGRAM_API_KEY, CHANNEL_ID


class TelegramChannel:
    def __init__(self):
        self.bot = telebot.TeleBot(TELEGRAM_API_KEY)

    def send_pdf(self, filename):
        with open(filename, "rb") as f:
            caption = "*Turni della settimana*"
            self.bot.send_document(
                CHANNEL_ID, f, caption=caption, parse_mode="markdown"
            )

    def send_turns(self, turns):
        yes_turns = list(filter(lambda x: x[1] > 0, turns))

        message = "\n".join(
            ["*Numero di turni per animatore*"]
            + list(map(lambda x: f"• {x[0]}: {x[1]}", yes_turns))
        )
        self.bot.send_message(CHANNEL_ID, message, parse_mode="markdown")

        no_turns = [name for name, _ in filter(lambda x: x[1] == 0, turns)]

        if len(no_turns) > 0:
            message = "\n".join(
                ["*Animatori con turno obbligatorio settimana prossima*"]
                + list(map(lambda x: f"• {x}", no_turns))
            )
            self.bot.send_message(CHANNEL_ID, message, parse_mode="markdown")

        with open("turni_obbligatori.txt", "w") as f:
            if len(no_turns) > 0:
                f.write("\n".join(["".join(name.split()) for name in no_turns]) + "\n")
