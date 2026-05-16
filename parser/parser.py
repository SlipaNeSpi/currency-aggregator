import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def fetch_cbr_rates():
    """Возвращает словарь с курсами USD и EUR от ЦБ РФ."""
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        rates = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code in ('USD', 'EUR'):
                value = float(valute.find('Value').text.replace(',', '.'))
                rates[char_code] = value
        return rates
    except Exception as e:
        print(f"Ошибка при получении курсов ЦБ РФ: {e}")
        return {}


def fetch_tinkoff_rates():
    """Возвращает курсы USD и EUR из открытого API Т-Банка."""
    url = "https://www.tinkoff.ru/api/v1/currency_rates/"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        rates = {}
        for item in data.get('payload', {}).get('rates', []):
            category = item.get('category', '')
            if category == 'DebitCardsTransfers':
                from_currency = item.get('fromCurrency', {}).get('name', '')
                to_currency = item.get('toCurrency', {}).get('name', '')
                if from_currency == 'USD' and to_currency == 'RUB':
                    buy = float(item.get('buy', 0))
                    sell = float(item.get('sell', 0))
                    if buy and sell:
                        rates['USD'] = round((buy + sell) / 2, 4)
                elif from_currency == 'EUR' and to_currency == 'RUB':
                    buy = float(item.get('buy', 0))
                    sell = float(item.get('sell', 0))
                    if buy and sell:
                        rates['EUR'] = round((buy + sell) / 2, 4)
        return rates
    except Exception as e:
        print(f"Ошибка при получении курсов Т-Банка: {e}")
        return {}


def fetch_all_rates():
    """Собирает курсы из всех источников и возвращает список словарей."""
    sources = [
        ('cbr', fetch_cbr_rates),
        ('tinkoff', fetch_tinkoff_rates)
    ]
    raw_data = []
    today = datetime.now().strftime('%Y-%m-%d')
    for source_name, fetcher in sources:
        rates = fetcher()
        for currency, rate in rates.items():
            raw_data.append({
                'source': source_name,
                'currency': currency,
                'rate': rate,
                'fetched_date': today
            })
    return raw_data


if __name__ == '__main__':
    from normalizer import normalize
    from db import insert_rates

    print("Сбор курсов валют...")
    raw = fetch_all_rates()
    clean = normalize(raw)
    print(f"Получено записей: {len(clean)}")
    insert_rates(clean)
    print("Готово.")