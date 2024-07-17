from django.shortcuts import render

# Create your views here.


def index(request):
    """Home page"""
    return render(request, 'screener/index.html')


def wallets(request):
    """page contains list of wallets"""
    return render(request, 'screener/wallets.html')


def addresses(request):
    """page contains wallet addresses"""
    return render(request, 'screener/addresses.html')


def about(request):
    """page contains site info"""
    return render(request, 'screener/about.html')


def contacts(request):
    """page contains ours contacts"""
    return render(request, 'screener/contacts.html')
