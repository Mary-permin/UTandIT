import telebot

API_token = "7129517966:AAHoD91o1tYV9bRiZ_addEjKx7vvkBs0Yqg"

bot = telebot.TeleBot(API_token)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the underground")


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.reply_to(message, "Нужна помощь? Хех\n \nЛааадно вот команды, которые ты можешь использовать:"
                          "\n /start\n /hello\n /anecdote\n /fnaf_lore"
                          "\n \n \nВот темы для разговора:"
                          "\n \n Спроси как у него дела\n Он с радостью даст тебе совет"
                          "\n Можешь правильно ответить на приветствие"
                          "\n Не общайся с ним про шкибиди туалеты, это даже для бота слишком💀"
                          "\n Про парней твоих подруг общаться он не будет"
                          "\n Undrtale - лучшая игра (просто факт)")


@bot.message_handler(commands=["hello"])
def send_welcome(message):
    bot.reply_to(message, f"{message.from_user.username}, я похож на куртака кобейна?🥰")


@bot.message_handler(commands=["anecdote"])
def send_welcome(message):
    bot.reply_to(message, "Идут два наркомана, видят курицу \n- это курица? \n- нет это естся")


@bot.message_handler(commands=["fnaf_lore"])
def send_welcome(message):
    bot.reply_to(message, "https://youtu.be/hkEkLM7HvW4?si=7VBxWknTxWvrkq1c")


@bot.message_handler(func=lambda massage:True)
def echo_massage(massage):
    text_massage = massage.text
    text_massage = text_massage.lower()
    if 'дела' in text_massage or "кд" in text_massage:
        bot.reply_to(massage, "Норм")
    elif "undertale" in text_massage:
        bot.reply_to(massage, "Опа опа опа андертуле\nЕсли ты любшь эту игру напиши мне: @Mary_permin")
    elif "Данил" in text_massage:
        bot.reply_to(massage, "Лучший мальчик, не оскорбляй его >:(")
    elif "совет" in text_massage:
        bot.reply_to(massage, "Совет дня: иди потрогай траву")
    elif "кибиди туалет" in text_massage or "skibidi toilet" in text_massage:
        bot.reply_to(massage, "💀")
    elif "Похож, только не заканчивай жизнь также" in text_massage:
        bot.reply_to(massage, "🥰")
    else:
        bot.reply_to(massage, "Хз ваще")



bot.infinity_polling()