from screener.models import Wallet, Address, TokenInfo
from .config_parse import list_of_support_chain
from .parse_data import get_token_amount_complete, get_prefix, get_price


def update_amount(user_id):
    """ Update staked, available and reward amount"""
    wallets = Wallet.objects.filter(wallet_owner=user_id)
    for wallet in wallets:
        for address in wallet.address_set.all():
            addr = Address.objects.get(address=address)
            prefix = get_prefix(str(address))
            if prefix in list_of_support_chain:
                data = get_token_amount_complete(user_address=address)
                addr.staked = data['info']['stake']
                addr.available = data['info']['available']
                addr.reward = data['info']['reward']
                addr.save()
            else:
                addr.staked, addr.reward, addr.reward = 'null', 'null', 'null'
    return 'Data is update'
    
    
def update_token_info_table():
    all_chains = TokenInfo.objects.all()
    for chain in all_chains:
        chain.current_price = get_price(chain.chain)
        chain.save()
    return 'Price for all chains update'
    
        
