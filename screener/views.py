from django.shortcuts import render, redirect, reverse
from .models import Wallet, Address
from .forms import WalletForm, AdressForm
from .services.parse_data import get_token_amount_complete
from .services.update_data import update_data


# Create your views here.


def index(request):
    """Home page"""
    context = {
        'text': update_data(request.user),
    }
    return render(request, 'screener/index.html', context)


def wallets(request):
    """page contains list of all wallets"""
    wallets = Wallet.objects.all()
    context = {'wallets': wallets}
    return render(request, 'screener/wallets.html', context)


def user_wallets(request):
    """page contains list of user wallets"""
    context = {
        'user_wallets': Wallet.objects.filter(wallet_owner=request.user)
    }
    return render(request, 'screener/user_wallets.html', context)


def user_wallet_info(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    addresses_list = wallet.address_set.all()
    context = {
        'info': get_token_amount_complete(addresses_list),
    }
    return render(request, 'screener/user_wallet_info.html', context)


def add_wallet(request):
    """Add wallet to user"""
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


def edit_portfolio(request, wallet_id):
    return render(request, 'screener/edit_portfolio.html')


def del_wallet(request, wallet_id):
    """Del user wallet"""
    wallet = Wallet.objects.get(id=wallet_id)
    wallet.delete()
    return redirect('screener:user_wallets')


def addresses(request, wallet_id):
    """page contains wallet addresses"""
    wallet = Wallet.objects.get(id=wallet_id)
    addresses = wallet.address_set.all()
    if addresses:
        context = {
            'addresses': addresses,
            'wallet': wallet
        }
    else:
        text = 'No added addresses'
        context = {
            'text': text,
            'wallet': wallet
        }
    return render(request, 'screener/addresses.html', context)


def address_info(request, address_id):
    address = Address.objects.get(id=address_id)
    context = {
        'staked': address.staked,
        'available': address.available,
        'reward': address.reward,
        'address': address
    }
    return render(request, 'screener/address_info.html', context)


def add_address(request, wallet_id):
    """Add address to user wallet"""
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
    """Delete address from user wallet"""
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
