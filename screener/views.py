from django.shortcuts import render
from .models import Wallet
from .services.parse_data import get_price
from .services.config_parse import name_of_token


# Create your views here.


def index(request):
    """Home page"""
    return render(request, 'screener/index.html')


def wallets(request):
    """page contains list of wallets"""
    wallets = Wallet.objects.all()
    context = {'wallets': wallets}
    return render(request, 'screener/wallets.html', context)


def addresses(request, wallet_id):
    """page contains wallet addresses"""
    wallet = Wallet.objects.get(id=wallet_id)
    addresses = wallet.address_set.all()
    price = dict()
    for add in addresses:
        chain = add.get_prefix()
        price[name_of_token[chain]] = get_price(chain)
    context = {
        'addresses': addresses,
        'price': price,
        'wallet': wallet,
        }
    return render(request, 'screener/addresses.html', context)


def about(request):
    """page contains site info"""
    return render(request, 'screener/about.html')


def contacts(request):
    """page contains ours contacts"""
    return render(request, 'screener/contacts.html')
