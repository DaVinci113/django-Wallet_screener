from django import forms
from .models import Wallet, Address
from django.core.exceptions import ValidationError
from screener.services.config_parse import list_of_support_chain


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['wallet_name']
        label = {'wallet_name': ''}


class AdressForm(forms.ModelForm):
    
    def clean_address(self):
        cleaned_data = super().clean()
        input_address = cleaned_data.get('address')
        
        if input_address[:-39] not in list_of_support_chain:
            raise ValidationError('Unsupported chain or incorrect address!')
        
        try:
            address = Address.objects.get(address=input_address)
            wallet_id = address.wallet_id
            wallet = Wallet.objects.get(pk=wallet_id)
            addresses = wallet.address_set.all()
            if any(addr for addr in addresses if str(addr) == input_address):
                raise ValidationError('Address is duplicate in this wallet!')
            
        except Address.DoesNotExist:
            return cleaned_data.get('address')
    
    class Meta:
        model = Address
        fields = ['address']
        label = {'address': ''}
