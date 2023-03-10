import telebot
from config import keys, TOKEN
from extensions import MoneyConverter, APIException


bot = telebot.TeleBot(TOKEN)  # создаю бота, токен из телеграма, который присвоил @BotFather


#  Обработчик функции help, start в телеграм боте
@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = "Что бы начать работу бота введите сообщение боту в формате:\n <имя валюты>_<в какую перевести>_<количество>\n \
            Пример: доллар рубль 5\n\
           Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
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
        text = f'Цена {amount} {quote.lower()} в {base.lower()} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)