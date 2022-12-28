import requests
import json
from config import keys, API_KEY


class APIException(Exception):
    pass


class MoneyConverter:
    """ Класс реализует функцию конвертации валют"""
    @staticmethod
    def get_price(quote: str, base: str, amount: str) -> float:

        if quote.lower() == base.lower():
            raise APIException(f'Недьзя конвертировать валюту {base} саму на себя')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key={API_KEY}')
        value = json.loads(r.content)
        result = quote_ticker + base_ticker
        total_base = round((float(value['data'][result]) * amount), 2)
        return total_base
