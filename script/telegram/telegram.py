import telebot

from environment import API_KEY, CHAT_ID


def main():
    bot = telebot.TeleBot(API_KEY)

    with open("turni.pdf", "rb") as f:
        caption = "Turni della settimana"
        bot.send_document(CHAT_ID, f, caption=caption)


if __name__ == "__main__":
    main()
