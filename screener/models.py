from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    wallet_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.wallet_name


class TokenInfo(models.Model):
    chain = models.CharField(max_length=20, unique=True, null=True, blank=True)
    current_price = models.FloatField(max_length=10, null=True, blank=True)


class Address(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    staked = models.FloatField(max_length=30, null=True, default='0', blank=True)
    available = models.FloatField(max_length=30, null=True, default='0', blank=True)
    reward = models.FloatField(max_length=30, null=True, default='0', blank=True)
    
    def __str__(self):
        return self.address
