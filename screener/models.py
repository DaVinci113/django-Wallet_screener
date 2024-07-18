from django.db import models

# Create your models here.


class Wallet(models.Model):
    wallet_name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.wallet_name
    
    
class Address(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    
    def __str__(self):
        return self.address
    
    def get_prefix(self):
        return str(self.address)[:-39]
    