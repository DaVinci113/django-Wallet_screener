from screener.models import Wallet, Address, TokenInfo
from .config_parse import list_of_support_chain
from .parse_data import get_token_amount_complete, get_prefix, get_price


def update_amount(user_id):
    """ Update staked, available and reward amount for user """
    all_addresses = Address.objects.all()
    for address_in_table in all_addresses:
        addr = Address.objects.get(address=address_in_table)
        prefix = get_prefix(str(address_in_table))
        if prefix in list_of_support_chain:
            data = get_token_amount_complete(address_in_table)
            addr.staked = data['info']['stake']
            addr.available = data['info']['available']
            addr.reward = data['info']['reward']
            addr.save()
        else:
            addr.staked, addr.reward, addr.reward = '0', '0', '0'
    return 'Data is update'
    
    
def update_token_info_table():
    all_chains = TokenInfo.objects.all()
    for chain in all_chains:
        try:
            chain.current_price = get_price(chain.chain)
            chain.save()
        except ValueError:
            chain.current_price = 0
    return 'Price for all chains update'
    
        
