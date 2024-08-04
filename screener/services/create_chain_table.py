from screener.models import TokenInfo
from .config_parse import list_of_support_chain


def get_table_fill():
    for chain in list_of_support_chain:
        token = TokenInfo()
        token.chain = chain
        token.save()
    return 'Table is created'
