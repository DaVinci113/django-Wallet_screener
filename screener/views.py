from django.shortcuts import render, redirect
from .models import Wallet, Address
from .forms import WalletForm, AdressForm
from .services.update_data import update_amount, update_token_info_table
from .services.download_data_from_db import wallet_data_db, address_data_db, user_portfolio_data_db, show_portfolio
from .services.create_chain_table import get_table_fill


# Create your views here.


def index(request):
    """Home page"""
    return render(request, 'screener/index.html')


def portfolio(request):
    wallet_data = user_portfolio_data_db(request.user)[0]
    all_amount = user_portfolio_data_db(request.user)[1]
    context = {
        'wallet_data': wallet_data,
        'all_amount': all_amount,
    }
    return render(request, 'screener/portfolio.html', context)


def wallets(request):
    """page contains list of all wallets"""
    wallets = Wallet.objects.all()
    context = {'wallets': wallets}
    return render(request, 'screener/wallets.html', context)


def user_wallets(request):
    """page contains list of user wallets"""
    context = {
        'user_wallets': Wallet.objects.filter(wallet_owner=request.user).select_related('wallet_owner')
    }
    return render(request, 'screener/user_wallets.html', context)


def user_wallet_info(request, wallet_id):
    wallet_data = wallet_data_db(wallet_id, dct=None)
    
    context = {
        'wallet_data': wallet_data,
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


def update(request):
    return render(request, 'screener/update.html')


def update_amount_data(request):
    """ update token amount for all user addresses """
    context = {
        'text': update_amount(request.user),
    }
    return render(request, 'screener/index.html', context)


def update_data(request):
    """ Update list of chain and price for all supported token """
    context = {
        'text': update_token_info_table(),
    }
    return render(request, 'screener/index.html', context)


def table_fill(request):
    context = {
        'text': get_table_fill()
    }
    return render(request, 'screener/index.html', context)


def address_info(request, address_id):
    address = Address.objects.get(id=address_id)
    context = {
        'data': address_data_db(address)
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


def testing(request):
    data = show_portfolio(request.user)
    context = {
        'data': data,
        'sum': data['portfolio_sum'],
        
    }
    return render(request, 'screener/testing.html', context)
    