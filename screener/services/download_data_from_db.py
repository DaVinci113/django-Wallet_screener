from screener.models import Wallet, Address


def address_data_db(user_address):
    address = Address.objects.get(address=user_address)
    return {
        'staked': address.staked,
        'available': address.available,
        'reward': address.reward,
    }


def wallet_data_db(user_wallet):
    wallet = Wallet.objects.get(id=user_wallet)
    addresses = wallet.address_set.all()
    wallet_data = {'wallet': wallet}
    for address in addresses:
        wallet_data[address] = address_data_db(address)
    return wallet_data
