import telebot


API_KEY = "API_KEY"
CHANNEL_ID = -1


def send_pdf(filename):
    bot = telebot.TeleBot(API_KEY)

    with open(filename, "rb") as f:
        caption = "*Turni della settimana*"
        bot.send_document(CHANNEL_ID, f, caption=caption, parse_mode="markdown")


def send_turns(turns):
    bot = telebot.TeleBot(API_KEY)

    counts = turns.get_animators_turns_counts(sort=True)
    message = '\n'.join(
        ["*Numero di turni per animatore*"]
        +
        list(map(
            lambda x : f"{x[0]}: {x[1]}",
            counts
        ))
    )
    bot.send_message(CHANNEL_ID, message, parse_mode="markdown")


if __name__ == "__main__":
    ...
