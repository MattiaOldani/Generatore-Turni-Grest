import telebot


API_KEY = "API_KEY"
CHANNEL_ID = -1


def send_pdf(filename):
    bot = telebot.TeleBot(API_KEY)

    with open(filename, "rb") as f:
        caption = "Turni della settimana"
        bot.send_document(CHANNEL_ID, f, caption=caption)


def send_turns(turns):
    ...


if __name__ == "__main__":
    ...
