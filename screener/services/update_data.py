from screener.models import Wallet, Address
from screener.services.parse_data import get_token_amount_complete


def update_data(user_id):
    wallets = Wallet.objects.filter(wallet_owner=user_id)
    for wallet in wallets:
        for address in wallet.address_set.all():
            data = get_token_amount_complete(user_address=address)
            addr = Address.objects.get(address=address)
            addr.staked = data['info']['stake']
            addr.available = data['info']['available']
            addr.reward = data['info']['reward']
            addr.save()
    return 'Data is update'
         
            