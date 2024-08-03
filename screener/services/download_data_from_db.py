from screener.models import Wallet, Address, TokenInfo
from screener.services.parse_data import get_prefix


def download_price(chain):
    token = TokenInfo.objects.get(chain=chain)
    return token.current_price
    
    
def address_data_db(user_address):
    address = Address.objects.get(address=user_address)
    prefix = get_prefix(str(address))
    staked = address.staked
    available = address.available
    reward = address.reward
    in_address = staked + available + reward
    price = download_price(prefix)
    return {
        'staked': staked,
        'available': available,
        'reward': reward,
        'all': in_address,
        'price': price,
        'coast': in_address * price,
    }


def wallet_data_db(user_wallet):
    wallet = Wallet.objects.get(id=user_wallet)
    addresses = wallet.address_set.all()
    wallet_data = {'wallet': wallet}
    for address in addresses:
        wallet_data[address] = address_data_db(address)
    return wallet_data


