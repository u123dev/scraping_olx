import re
from datetime import datetime

import pytz


def convert_to_date(date_string: str) -> datetime:
    months = {
        "січня": "January",
        "лютого": "February",
        "березня": "March",
        "квітня": "April",
        "травня": "May",
        "червня": "June",
        "липня": "July",
        "серпня": "August",
        "вересня": "September",
        "жовтня": "October",
        "листопада": "November",
        "грудня": "December",
        "января": "January",
        "февраля": "February",
        "марта": "March",
        "апреля": "April",
        "мая": "May",
        "июня": "June",
        "июля": "July",
        "августа": "August",
        "сентября": "September",
        "октября": "October",
        "ноября": "November",
        "декабря": "December"
    }

    if "Сьогодні" in date_string  or "Сегодня" in date_string:
        date_str = datetime.now().strftime("%d %B %Y") + " " + date_string[-5:]  # concat current date + time
    else:
        date_str = date_string.replace(" г.", "").replace(" р.", "") + " 00:00"
        for cyr_month, eng_month in months.items():
            date_str = date_str.replace(cyr_month, eng_month)  # cyr2eng month

    date_obj = datetime.strptime(date_str, "%d %B %Y %H:%M")  # str2obj

    kiev_tz = pytz.timezone("Europe/Kiev")
    return pytz.utc.localize(date_obj).astimezone(kiev_tz)

def convert_to_num(num_str: str) -> (int, str):
    if num_str is None:
        num_str = ""

    match = re.match(r"([0-9\s]+)\s*([^\d]+)", num_str.strip())
    if match:
        amount = int(match.group(1).replace(" ", ""))
        currency = match.group(2).strip()
        return amount, currency
    else:
        return None, None
