import requests
from bs4 import BeautifulSoup
from .config_parse import params, headers, headers_ng, cookies, name_of_chain, name_of_token, devision
import time


def address_to_chain(address):
    return address[:-39]


def get_prefix(address):
    return address[:-39]


def get_address(address):
    return address[-39::]


def get_price(prefix):
    time.sleep(0.1)
    response = requests.get(
        f'https://coinmarketcap.com/currencies/{name_of_chain[prefix]}/',
        cookies=cookies,
        headers=headers,
    )
    soup = BeautifulSoup(response.text)
    price = soup.find(class_='sc-65e7f566-0 clvjgF base-text').text
    return price[1::]


def get_token_amount_cosmostation(chain, user_address):
    
    try:
        time.sleep(0.1)
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
            stake += float(response_staked['delegation_responses'][i]['balance']['amount']) / devision[chain]
            reward += float(response_reward['rewards'][i]['reward'][-1]['amount']) / devision[chain]
        
        available = float(response_available['balances'][-1]['amount']) / devision[chain]
        
        return {
            'stake': stake,
            'available': available,
            'reward': reward
        }
    except Exception as ex:
        return ex
    
    
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
        return ex


def get_token_amount_complete(user_address):
    user_address = user_address.address
    prefix = get_prefix(user_address)
    chain = name_of_chain[prefix]
    price = get_price(prefix)
    try:
        return {
            'info': get_token_amount_cosmostation(chain=chain, user_address=user_address),
            'price': price,
        }
    except Exception:
        return {
            'info': get_token_amount_guru(chain=chain, user_address=user_address),
            'price': price,
        }
            
            
        
