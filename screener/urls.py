from django.urls import path
from . import views


app_name = 'screener'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # page contains list of user wallets
    path('user_wallets/', views.user_wallets, name='user_wallets'),
    
    # page contains wallet addresses
    path('addresses/<int:wallet_id>', views.addresses, name='addresses'),
    
    # page contains site info
    path('about/', views.about, name='about'),
    
    # page contains ours contacts
    path('contacts/', views.contacts, name='contacts'),
]
