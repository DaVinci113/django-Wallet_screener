import requests
from bs4 import BeautifulSoup
from .config_parse import params, headers, headers_ng, cookies, name_of_chain, devision, time_out
import aiohttp
import asyncio
import time


def get_prefix(user_address):
    return str(user_address)[:-39]


def get_price(prefix):
    try:
        time.sleep(time_out)
        response = requests.get(
            f'https://coinmarketcap.com/currencies/{name_of_chain[prefix]}/',
            cookies=cookies,
            headers=headers,
        )
        soup = BeautifulSoup(response.text)
        price = soup.find(class_='sc-65e7f566-0 clvjgF base-text').text
        return price[1::]
    except Exception:
        return 0


def get_token_amount_cosmostation(chain, user_address, prefix):
    
    try:
        time.sleep(time_out)
        response_staked = requests.get(
            f'https://lcd-{chain}.cosmostation.io/cosmos/staking/v1beta1/delegations/{user_address}',
            params=params,
            headers=headers,
        ).json()
        response_available = requests.get(
            f'https://lcd-{chain}.cosmostation.io/cosmos/bank/v1beta1/balances/{user_address}',
            params=params,
            headers=headers,
        ).json()
        response_reward = requests.get(
            f'https://lcd-{chain}.cosmostation.io/cosmos/distribution/v1beta1/delegators/{user_address}/rewards',
            params=params,
            headers=headers,
        ).json()
        stake = 0
        reward = 0
        
        length = len(response_staked['delegation_responses'])
        
        for i in range(length):
            stake += float(response_staked['delegation_responses'][i]['balance']['amount']) / devision[prefix]
            reward += float(response_reward['rewards'][i]['reward'][-1]['amount']) / devision[prefix]
        
        available = float(response_available['balances'][-1]['amount']) / devision[prefix]
        
        return {
            'stake': stake,
            'available': available,
            'reward': reward
        }
    except Exception as ex:
        return {
            'stake': 0,
            'available': 0,
            'reward': 0,
        }
    
    
def get_token_amount_guru(chain, user_address):
    try:
        response = requests.get(
            f'https://{chain}.api.explorers.guru/api/v1/accounts/{user_address}/balance',
            headers=headers_ng,
        ).json()
        stake = float(response['balance']['delegated']['amount']) / devision[chain]
        available = float(response['balance']['spendable']['amount']) / devision[chain]
        reward = float(response['balance']['reward']['amount']) / devision[chain]
        return {
            'stake': stake,
            'available': available,
            'reward': reward
        }
    
    except Exception as ex:
        return {
            'stake': 0,
            'available': 0,
            'reward': 0,
        }


def get_token_amount_complete(user_address):
    user_address = user_address.address
    prefix = get_prefix(user_address)
    chain = name_of_chain[prefix]
    try:
        return {
            'info': get_token_amount_cosmostation(chain=chain, user_address=user_address, prefix=prefix),
        }
    except Exception as ex:
        return {
            'info': get_token_amount_guru(chain=chain, user_address=user_address),
        }
            
        

