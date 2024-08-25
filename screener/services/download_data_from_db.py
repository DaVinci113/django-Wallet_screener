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
        # 'chain': prefix,
        'address': user_address,
        'staked': staked,
        'available': available,
        'reward': reward,
        'all': in_address,
        'price': price,
        'coast': in_address * price,
    }


def wallet_data_db(wallet_id, dct=None):
    wallet = Wallet.objects.get(id=wallet_id)
    user_addresses = wallet.address_set.all().select_related('wallet')
    wallet_data = {'wallet $': int(), 'wallet': wallet}
    for user_address in user_addresses:
        chain = get_prefix(user_address)
        wallet_data[chain] = address_data_db(user_address)
        wallet_data['wallet $'] += wallet_data[chain]['coast']
        if dct is not None:
            if chain not in dct:
                dct[chain] = {
                    'staked': int(),
                    'available': int(),
                    'reward': int(),
                    'all': int(),
                }
            dct[chain]['staked'] += wallet_data[chain]['staked']
            dct[chain]['available'] += wallet_data[chain]['available']
            dct[chain]['reward'] += wallet_data[chain]['reward']
            dct[chain]['all'] += wallet_data[chain]['all']
    return wallet_data, dct


def user_portfolio_data_db(user):
    user_wallets = Wallet.objects.filter(wallet_owner=user).select_related('wallet_owner')
    portfolio_data = {'portfolio_sum': int()}
    portfolio_amount_info = {}
    for user_wallet in user_wallets:
        all_info = wallet_data_db(user_wallet.id, dct=portfolio_amount_info)
        portfolio_data[user_wallet] = all_info[0]
        portfolio_data['portfolio_sum'] += all_info[0]['wallet $']
        # portfolio_data[user_wallet] = wallet_data_db(user_wallet.id, dct=portfolio_amount_info)[0]
        # portfolio_data['portfolio $'] += portfolio_data[user_wallet]['wallet $']
    return portfolio_data, all_info[1]


def show_portfolio(user):
    user_wallets = Wallet.objects.filter(wallet_owner=user).select_related('wallet_owner')
    dct = {'portfolio_sum': int()}
    for user_wallet in user_wallets:
        wallet_info = {'wallet_sum': int()}
        user_addresses = user_wallet.address_set.all().select_related('wallet')
        for user_address in user_addresses:
            chain = get_prefix(str(user_address))
            staked = user_address.staked
            available = user_address.available
            reward = user_address.reward
            in_address = staked + available + reward
            token = TokenInfo.objects.get(chain=chain)
            price = token.current_price
            
            address_info = {
                'chain': chain,
                'address': user_address,
                'staked': staked,
                'available': available,
                'reward': reward,
                'all': in_address,
                'price': price,
                'cost': in_address * price,
            }
            wallet_info[user_address] = address_info
            wallet_info['wallet_sum'] += address_info['cost']
        dct[user_wallet] = wallet_info
        dct['portfolio_sum'] += wallet_info['wallet_sum']
    return dct
