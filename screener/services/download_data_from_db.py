from screener.models import Wallet, Address, TokenInfo
from screener.services.parse_data import get_prefix


def download_price() -> dict:
    """Download TokenInfo table"""
    return TokenInfo.objects.values()


def address_data_db(user_address: str, tokens_price: dict) -> dict:
    chain = get_prefix(str(user_address))
    for token_price in tokens_price:
        if token_price['chain'] == chain:
            staked = user_address.staked
            available = user_address.available
            reward = user_address.reward
            in_address = staked + available + reward
            price = token_price['current_price']
            address_info = {
                'chain': chain,
                'address': user_address,
                'staked': staked,
                'available': available,
                'reward': reward,
                'all': in_address,
                'price': price,
                'cost': round(in_address * price, 2)
            }
    return address_info


def wallet_data_db(wallet_id: int) -> dict:
    tokens_price = download_price()
    wallet = Wallet.objects.get(id=wallet_id)
    user_addresses = wallet.address_set.all().select_related('wallet')
    wallet_info = {'wallet_sum': int()}
    for user_address in user_addresses:
        address_info = address_data_db(user_address=user_address, tokens_price=tokens_price)
        wallet_info[user_address] = address_info
        wallet_info['wallet_sum'] += address_info['cost']
    return wallet_info


def portfolio_data_db(user: int) -> dict:
    tokens_price = download_price()
    user_wallets = Wallet.objects.filter(wallet_owner=user)
    portfolio_info = {'portfolio_sum': int()}
    all_amount = dict()
    for user_wallet in user_wallets:
        wallet_info = {'wallet_sum': int()}
        user_addresses = user_wallet.address_set.all()
        for user_address in user_addresses:
            chain = str(user_address)[:-39]
            if chain not in all_amount:
                all_amount[chain] = {
                    'staked': 0,
                    'available': 0,
                    'reward': 0,
                    'all': 0,
                    'cost': 0,
                }
            address_info = address_data_db(user_address=user_address, tokens_price=tokens_price)
            all_amount[chain]['staked'] += address_info['staked']
            all_amount[chain]['available'] += address_info['available']
            all_amount[chain]['reward'] += address_info['reward']
            all_amount[chain]['all'] += address_info['all']
            all_amount[chain]['cost'] += address_info['cost']
            wallet_info[user_address] = address_info
            wallet_info['wallet_sum'] += address_info['cost']
        portfolio_info[user_wallet] = wallet_info
        portfolio_info['portfolio_sum'] += wallet_info['wallet_sum']
    return portfolio_info, all_amount
