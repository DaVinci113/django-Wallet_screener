from django.db import models
from django.contrib.auth.models import User
from .services.config_parse import name_of_token, name_of_chain
from .services.parse_data import get_price
from django.shortcuts import reverse


# Create your models here.


class Wallet(models.Model):
    wallet_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.wallet_name
    
    
class Address(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.address
