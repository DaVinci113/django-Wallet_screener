from django import forms
from .models import Wallet, Address


class WalletForm(forms.ModelForm):

    class Meta:
        model = Wallet
        fields = ['wallet_name']
        label = {'wallet_name': ''}
        
        
class AdressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ['address']
        label = {'address': ''}
    