import telebot
from telebot import types
from googletrans import Translator
from gtts import gTTS
import random
token = '6571514893:AAHrNlQfNVKFwqpTVycYYyV4h6_7MBL0jcU'
bot = telebot.TeleBot(token)
translator = Translator()

with open("vocab.txt",'r',encoding = 'utf-8') as f:
  vocab = f.readlines()
score = 0
lang = ['английский',"испанский",'немецкий','французский']

def question(message):
    global word, word_de, word_en, word_es, lang_c, word_fr
    temp = random.choice(vocab) # выбираем случайное слово из 1000 возможных
    word = temp[:-1] # берем все слово кроме последнего символа(пробела)
    word_en = translator.translate(text=word,src='ru',dest='en').text.capitalize()
    word_es = translator.translate(text=word,src='ru',dest='es').text.capitalize()
    word_de = translator.translate(text=word,src='ru',dest='de').text.capitalize()
    word_fr = translator.translate(text=word,src='ru',dest='fr').text.capitalize()

    lang_c = random.choice(lang) # берем случайный язык
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)


    item1 = types.KeyboardButton(word_en)
    item2 = types.KeyboardButton(word_es)
    item3 = types.KeyboardButton(word_de)
    item4 = types.KeyboardButton(word_fr)

    list_of_buttons = [item1, item2, item3, item4]

    for i in range(4):
        random_button = random.choice(list_of_buttons) # сохраняем в переменную случайную кнопку
        markup.add(random_button) # добавляем ее в клавиатуру
        list_of_buttons.remove(random_button) # удаляем из списка кнопок чтобы она не добавилась еще раз
        
    bot.send_message(message.chat.id, f"Как переводится {word} на {lang_c} язык? ",reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    question(message)  

@bot.message_handler(content_types='text')
def do(message):
    global score, lang_c
    if (lang_c == 'английский' and message.text == word_en) or (lang_c == 'испанский' and message.text == word_es) or (lang_c == 'немецкий' and message.text == word_de) or (lang_c == 'французский' and message.text == word_fr):
        score += 1
        bot.send_message(message.chat.id, f"Правильно! Счёт: {str(score)}")
    else:
        score -= 1
        bot.send_message(message.chat.id, f"Ошибка! Счёт: {str(score)}")
    question(message)

bot.polling(none_stop = True)