from screener.models import Wallet
import requests
from bs4 import BeautifulSoup
from .config_parse import headers_price, name_of_chain
import time

def address_to_chain(address):
    return address[:-39]


def get_amount_data():
    pass


def get_price(prefix):
    time.sleep(0.1)
    response = requests.get(f'https://coinmarketcap.com/currencies/{name_of_chain[prefix]}/', headers=headers_price)
    soup = BeautifulSoup(response.text)
    data = soup.find('div', class_='sc-d1ede7e3-0 gNSoet flexStart alignBaseline')
    price = data.find('span').text
    return price[1::]
