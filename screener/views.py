from django.shortcuts import render, redirect, reverse
from .models import Wallet, Address
from .services.parse_data import get_price
from .services.config_parse import name_of_token
from .forms import WalletForm, AdressForm


# Create your views here.


def index(request):
    """Home page"""
    return render(request, 'screener/index.html')


def wallets(request):
    """page contains list of wallets"""
    wallets = Wallet.objects.all()
    context = {'wallets': wallets}
    return render(request, 'screener/wallets.html', context)


def user_wallets(request):
    context = {
        'user_wallets': Wallet.objects.filter(wallet_owner=request.user)
    }
    return render(request, 'screener/user_wallets.html', context)
    

def add_wallet(request):
    if request.method != 'POST':
        form = WalletForm()
    else:
        form = WalletForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.wallet_owner = request.user
            form.save()
            return redirect('screener:user_wallets')
    context = {'form': form}
    return render(request, 'screener/add_wallet.html', context)


def del_wallet(request, wallet_id):
    wallet = Wallet.objects.filter(id=wallet_id)
    if request.method == 'DELETE':
        wallet.delete()
    


def addresses(request, wallet_id):
    """page contains wallet addresses"""
    wallet = Wallet.objects.get(id=wallet_id)
    addresses = wallet.address_set.all()
    if addresses:
        price = dict()
        for add in addresses:
            chain = add.get_prefix()
            price[name_of_token[chain]] = get_price(chain)
        context = {
            'addresses': addresses,
            'price': price,
            'wallet': wallet,
            }
    else:
        add_some_address = 'Add some address'
        context = {
            'Add some address': add_some_address,
            'wallet': wallet
        }
    return render(request, 'screener/addresses.html', context)


def add_address(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    if request.method != 'POST':
        form = AdressForm()
    else:
        form = AdressForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.wallet = wallet
            form.save()
            return redirect('screener:addresses', wallet_id=wallet.id)
    context = {
        'form': form,
        'wallet': wallet,
    }
    return render(request, 'screener/add_address.html', context)


def del_address(request, address_id):
    address = Address.objects.get(id=address_id)
    wallet_id = address.wallet_id
    address.delete()
    return redirect('screener:addresses', wallet_id)


def about(request):
    """page contains site info"""
    return render(request, 'screener/about.html')


def contacts(request):
    """page contains ours contacts"""
    return render(request, 'screener/contacts.html')
