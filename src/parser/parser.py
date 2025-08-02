import requests
from bs4 import BeautifulSoup
from datetime import datetime


def clear_price(price: str) -> int:
    if price == '—':
        return 0
    return int(''.join(price[:-2].split()))


def go_to_date(time: str, start: bool = True) -> datetime:
    if start:
        # Обработка даты начала торгов (она без времени)
        return datetime.strptime(time, "%d.%m.%Y")
    try:
        # Обработка даты конца торгов (если есть время)
        return datetime.strptime(time, "%d.%m.%Y %H:%M")
    except ValueError:
        try:
            # Обработка даты конца торгов (если есть нет времени). Обрезаю строку т.к приходит в виде '02.08.2025 '
            return datetime.strptime(time[:-1], "%d.%m.%Y")
        except Exception as e:
            print(f"Ошибка парсинга даты: {time}, {e}")
            return None


def parser(count: int) -> list[dict]:

    url = "https://rostender.info/extsearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all("article", class_="tender-row row")

        result = []

        for article in articles[:count]:
            tender = {}

            number = article.find(
                "span", class_="tender__number").get_text(strip=True)
            number = int(number[number.find('№')+1:])  # Обрезаю лишний текст

            date_start = article.find(
                "span", class_="tender__date-start").get_text(strip=True)
            date_start = date_start[date_start.find('т')+2:]  # Обрезаю "от "
            # было '02.08.25' стало '02.08.2025'
            date_start = go_to_date(date_start[:6] + "20" + date_start[6:])

            date_end = article.find(
                "span", class_="tender__countdown-text").get_text(strip=True)
            date_end_day = go_to_date(date_end[date_end.find(
                ')')+1:date_end.find(')')+11] + ' ' + date_end[date_end.find(')')+11:], start=False)

            decription = article.find(
                "a", class_="description tender-info__description tender-info__link")
            decription_text = decription.get_text(strip=True)
            link = f"https://rostender.info{decription['href']}"

            start_price = clear_price(article.find(
                "div", class_="starting-price__price starting-price--price").get_text(strip=True))

            adress = article.find("div", class_="tender-address").find(
                "div", class_="line-clamp line-clamp--n3").get_text(strip=True)

            tender["Номер тендера"] = number
            tender["Начало торгов"] = date_start
            tender["День окончания торгов"] = date_end_day
            tender["Название тендера"] = decription_text
            tender["Ссылка на тендер"] = link
            tender["Начальная цена"] = start_price
            tender["Город"] = adress

            result.append(tender)

        return result
    except Exception as e:
        return (f"Ошибка: {e}")
