import telebot
from telebot import types
from config import keys, TOKEN
from extensions import MoneyConverter, APIException


bot = telebot.TeleBot(TOKEN)  # токен из телеграма @BotFather


#  Обработчик функции help, start в телеграм боте
@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = "Что бы начать работу бота введите сообщение боту в формате:\n <имя валюты>_<в какую перевести>_<количество>\n \
            Пример: доллар рубль 5\n\
           Увидеть список всех доступных валют: /values"
    buttons = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('доллар рубль 1')
    btn2 = types.KeyboardButton('евро рубль 1')
    btn3 = types.KeyboardButton('йена рубль 1')
    buttons.row(btn1, btn2, btn3)
    btn4 = types.KeyboardButton('рубль доллар 100')
    btn5 = types.KeyboardButton('рубль евро 100')
    btn6 = types.KeyboardButton('рубль йена 100')
    buttons.row(btn4, btn5, btn6)
    bot.reply_to(message, text)
    bot.send_message(message.chat.id, f"Готов начать работать\nID нашего чата:{message.chat.id}", reply_markup=buttons)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные боту валюты:'
    btn = types.InlineKeyboardMarkup()
    btn.add(types.InlineKeyboardButton('Вся инфа на сайте', url='https://currate.ru'))
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text, reply_markup=btn)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    btn = types.InlineKeyboardMarkup()
    btn.add(types.InlineKeyboardButton('Удалить последний запрос', callback_data='remove'))
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров!')

        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'ошибка пользователя {e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду {e}')
    else:
        text = f'Цена {amount} {quote.lower()} в {base.lower()} = {total_base}'
        bot.send_message(message.chat.id, text,  reply_markup=btn)


@bot.callback_query_handler(func=lambda callback: True)
def callback_func(callback):
    if callback.data == 'remove':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)


@bot.message_handler(content_types=['photo', 'audio', 'video'])
def photo_format(message: telebot.types.Message):
    bot.reply_to(message, 'Хорошая, но что мне с этим делать?\nЯ работаю с текстовым контентом\n/help или /values')


print(".....I am working now.....")
bot.polling(none_stop=True)
