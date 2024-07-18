import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv, find_dotenv
import os
from bs4 import BeautifulSoup
from g4f.client import Client
import curl_cffi
from generate_img_with_sber import gen_img

load_dotenv(find_dotenv())
API_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(API_TOKEN)


def info_wolfram(query):
    client = Client()
    response = client.chat.comption.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content


@bot.message_handler(commands=["create_img"])
def photo(message):
    bot.send_message(message.chat.id, "Отправте описание картинкиы")
    bot.register_next_step_handler(message, send_den_img)


def send_den_img(message):
    try:
        content = gen_img(message.text, "3E3B5F5C69F1A16059026C329001C794",
                          "657537579F4DA135F05A1C63127E710C")
        bot.send_photo(message.chat.id, content)
    except:
        bot.send_message(message.chat.id, "Извините не понял вас")
def get_into_word(word):
    url = f"https://ru.wiktionary.org/wiki/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    answer = soup.find('ol')
    return answer.text


@bot.message_handler(commands=["word_meaning"])
def word_meaning(message):
    chatID = message.from_user.id
    bot.send_message(chatID, "Какое слово тебе не понятно?")
    bot.register_next_step_handler(message, word_mean)


def word_mean(message):
    chatID = message.from_user.id
    word = message.text.lower()
    bot.send_message(chatID, get_into_word(word))


def get_temperature(lat, lon):
    print(1)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"

    response = requests.get(url)
    print(2)
    if response.status_code == 200:
        data = response.json()
        current_temp=str(data["current"]["temperature_2m"])
        print(3)
        return current_temp
    else:
        print(f"Ошибка: {response.status_code}")
        return "не удолось определить погоду"



session = {}


@bot.message_handler(commands=["location"])
def weather(message):
    chatID = message.from_user.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    key = KeyboardButton(text = "отправить геопозицию", request_location=True)
    markup.add(key)
    bot.send_message(chatID, "Пожалуйста отправте геопозицию", reply_markup=markup)
    bot.register_next_step_handler(message, weather1)


def weather1(message):
    chatID = message.from_user.id
    lat = message.location.latitude
    lon = message.location.longitude
    current_wether = get_temperature(lat, lon)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(chatID, f"Там температура {current_wether}", reply_markup=markup)




@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the underground")


# @bot.message_handler(commands=["knopki"])
# def knopki(message):
#     chatID = message.from_user.id
#     markup = InlineKeyboardMarkup()
#     button1 = InlineKeyboardButton("мем", callback_data='meme')
#     button2 = InlineKeyboardButton("реальность", callback_data="image")
#     markup.add(button1)
#     markup.add(button2)
#     bot.send_message(chatID, "Выбери картинку по андертейлу", reply_markup=markup)
#
#
# @bot.callback_query_handlers(func=lambda callback: True)
# def handle_callback(callback):
#     chatID = callback.message.from_user.id
#     button_call = callback.data
#     if button_call == "meme":
#         bot.send_photo(chatID, "https://i.pinimg.com/736x/3f/a8/85/3fa885623122bae1894dc139bb69a14c.jpg")
#     elif button_call == "image":
#         bot.send_photo(chatID, "https://img.wattpad.com/c6f4b38a0033b2dea34eb4baa669b10b9fc536d1/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f307137345f566f756d5a78767a673d3d2d3238353638303639312e313436323439363665393535356161333932383031303634353236372e6a7067?s=fit&w=720&h=720")
# session = {}
#
#
# @bot.message_handler(commands=["anketa"])
# def start_anketa(message):
#     chatID = message.from_user.id
#     bot.send_message(chatID, "Введите ваше имя")
#     bot.register_next_step_handler(message, anketa1)
#
#
# def anketa1(message):
#     chatID = message.from_user.id
#     try:
#         session[chatID]['Name'] = message.text
#         bot.send_message(chatID, "Введите возраст")
#         bot.register_next_step_handler(message, anketa2)
#     except:
#         bot.send_message(chatID, "Возможно вы не ввели команду старт")
#
#
# def anketa2(message):
#     chatID = message.from_user.id
#     try:
#         session[chatID]["Age"] = int(message.text)
#         bot.send_message(chatID, "Анкета заполнена")
#         bot.register_next_step_handler(message, anketa2)
#     except:
#         bot.send_message(chatID, "Введите ваш возраст в виде числа")
#         bot.register_next_step_handler(message, anketa2)
#

@bot.message_handler(commands=["buttons"])
def button(message):
    chatID = message.from_user.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Яблоко", "Груша", "Банан", "Ананас", row_width=2)
    bot.send_message(chatID, "Кнопычки", reply_markup=markup)


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.reply_to(message, "Нужна помощь? Хех\n \nЛааадно вот команды, которые ты можешь использовать:"
                          "\n /start\n /hello\n /anecdote\n /fnaf_lore\n"
                          "\n /random1 /random2 /random3\n /stiker\n /pon\n /meme\n /more_meme" 
                          "\n \n \nВот темы для разговора:"
                          "\n \n Спроси как у него дела\n Он с радостью даст тебе совет"
                          "\n Можешь правильно ответить на приветствие"
                          "\n После старта можешь продолжить песню"
                          "\n Не общайся с ним про шкибиди туалеты, это даже для бота слишком💀"
                          "\n Undertale - лучшая игра (просто факт)")


@bot.message_handler(commands=["hello"])
def send_welcome(message):
    bot.reply_to(message, f"{message.from_user.username}, я похож на курта кобейна?🥰")


@bot.message_handler(commands=["anekdot"])
def anekdot(message):
    bot.reply_to(message, "Идут два наркомана, видят курицу \n- это курица? \n- нет это естся")


@bot.message_handler(commands=["fnaf_lore"])
def send_welcome(message):
    bot.reply_to(message, "https://youtu.be/hkEkLM7HvW4?si=7VBxWknTxWvrkq1c")


@bot.message_handler(commands=["random1"])
def random1(message):
    chatID = message.from_user.id
    bot_massage = bot.send_dice(chatID, "🎰")


@bot.message_handler(commands=["random2"])
def random1(message):
    chatID = message.from_user.id


@bot.message_handler(commands=["random3"])
def random1(message):
    chatID = message.from_user.id
    bot_massage = bot.send_dice(chatID, "🏀")


@bot.message_handler(commands=["stiker"])
def stiker(message):
    chatID = message.from_user.id
    bot_massage = bot.send_sticker(chatID, "CAACAgUAAxkBAAJlsGaWSi-9_hlkzW33MO9z_cRMhqqWAAKvCAAC-poxVsixiRYkTCNjNQQ")


@bot.message_handler(commands=["pon"])
def pon(message):
    chatID = message.from_user.id
    bot_massage = bot.send_sticker(chatID, "CAACAgIAAxkBAAJlvGaWSzQB94egoJJVL1miiEY_XoEMAAJzGQACzoAJSeNSYlV59JjXNQQ")


@bot.message_handler(commands=["meme"])
def img(message):
        chatID = message.from_user.id
        bot_massage = bot.send_photo(chatID, "https://i.pinimg.com/736x/64/0b/d4/640bd4592d754ca6f8d827e83eb8c06e.jpg")


@bot.message_handler(commands=["more_meme"])
def video(message):
    chatID = message.from_user.id
    bot_message = bot.send_video(chatID, open("kromer_meme.mp4", "rb"))


@bot.message_handler(func=lambda massage:True)
def echo_massage(massage):
    text_massage = massage.text
    text_massage = text_massage.lower()
    if 'дела' in text_massage or "кд" in text_massage:
        bot.reply_to(massage, "Норм")
    elif "undertale" in text_massage:
        bot.reply_to(massage, "Опа опа опа андертуле\nЕсли ты любшь эту игру напиши мне: @Mary_permin")
    elif "данил" in text_massage:
        bot.reply_to(massage, "Лучший мальчик, не оскорбляй его >:(")
    elif "совет" in text_massage:
        bot.reply_to(massage, "Совет дня: иди потрогай траву")
    elif "кибиди туалет" in text_massage or "skibidi toilet" in text_massage:
        bot.reply_to(massage, "💀")
    elif "похож, только не заканчивай жизнь также" in text_massage:
        bot.reply_to(massage, "🥰")
    elif "how was the fall" in text_massage or "how was a fall" in text_massage:
        bot.reply_to(massage, "If you wanna look around")
    elif "how are your balls" in text_massage:
        bot.reply_to(massage, "If you wanna look around?..")
    elif "give us a call" in text_massage or "give us the call" in text_massage:
        bot.reply_to(massage, "Ценитель классики")
    elif "give us your balls" in text_massage or "GIVE US YOUR BALLS" in text_massage:
        bot.reply_to(massage, "Настоящий ценитель классики💀")
    else:
        bot.reply_to(massage, "Хз ваще")



bot.infinity_polling()