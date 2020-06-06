import requests
from bs4 import BeautifulSoup
import random

# import csv

HEADS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'accept': '*/*'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADS, params=params)
    r.encoding = 'UTF-8'
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Находим все элементы в главном div с классом vacancy-serp-item
    items = soup.find_all(
        'div',
        class_='vacancy-serp-item',
        limit=50)
    links = []
    five = []
    # Из всех элементов ищем a с классом bloko-link HH-LinkModifier
    for item in items:
        links.append([
            item.find('a', class_='bloko-link HH-LinkModifier').get_text(),
            item.find('a', class_='bloko-link HH-LinkModifier').get('href')
            ])
    if len(links) == 0:
        return links
    while len(five) < 5:
        x = random.choice(links)
        if x not in five:
            five.append(x)
    return five


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print('ERROR')