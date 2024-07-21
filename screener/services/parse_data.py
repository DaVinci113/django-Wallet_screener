import requests
from bs4 import BeautifulSoup
from .config_parse import headers, cookies, name_of_chain
import time


def address_to_chain(address):
    return address[:-39]


def get_amount_data():
    pass


def get_price(prefix):
    time.sleep(0.2)
    response = requests.get(
        f'https://coinmarketcap.com/currencies/{name_of_chain[prefix]}/',
        cookies=cookies,
        headers=headers,
    )
    soup = BeautifulSoup(response.text)
    price = soup.find(class_='sc-65e7f566-0 clvjgF base-text').text
    return price[1::]
