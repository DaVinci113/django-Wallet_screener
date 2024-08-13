from screener.models import Wallet, Address, TokenInfo
from screener.services.parse_data import get_prefix


def download_price(chain):
    token = TokenInfo.objects.get(chain=chain)
    return token.current_price


def address_data_db(user_address):
    user_address = Address.objects.get(address=user_address)
    prefix = get_prefix(str(user_address))
    staked = user_address.staked
    available = user_address.available
    reward = user_address.reward
    in_address = staked + available + reward
    price = download_price(prefix)
    return {
        'chain': prefix,
        # 'address': user_address,
        'staked': staked,
        'available': available,
        'reward': reward,
        'all': in_address,
        'price': price,
        'coast': in_address * price,
    }


def wallet_data_db(user_wallet):
    wallet = Wallet.objects.get(id=user_wallet)
    user_addresses = wallet.address_set.all()
    wallet_data = {'wallet $': int(), 'wallet': wallet}
    for user_address in user_addresses:
        wallet_data[user_address] = address_data_db(user_address)
        wallet_data['wallet $'] += wallet_data[user_address]['coast']
    return wallet_data


def user_portfolio_data_db(user):
    user_wallets = Wallet.objects.filter(wallet_owner=user)
    chain_amount_wallet = {}
    portfolio_data = {
        'portfolio $': int(),
    }
    for user_wallet in user_wallets:
        portfolio_data[user_wallet] = wallet_data_db(user_wallet.id)
        portfolio_data['portfolio $'] += portfolio_data[user_wallet]['wallet $']
        # chain_amount_wallet[portfolio_data[user_wallet]['chain']] =
        #
        # chain_amount_wallet[portfolio_data[user_wallet]['chain']]['available'] += portfolio_data[user_wallet]['available']
        # chain_amount_wallet[portfolio_data[user_wallet]['chain']]['reward'] += portfolio_data[user_wallet]['reward']
    return portfolio_data

