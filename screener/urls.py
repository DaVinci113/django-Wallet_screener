from django.urls import path
from . import views


app_name = 'screener'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # page contains list of user wallets
    path('user_wallets/', views.user_wallets, name='user_wallets'),
    
    # page contains wallet addresses
    path('user_wallets/addresses/<int:wallet_id>/', views.addresses, name='addresses'),
    
    # info about wallet
    path('user_wallets/user_wallet_info/<int:wallet_id>/', views.user_wallet_info, name='user_wallet_info'),
    
    # page contains address info
    path('address_info/<int:address_id>/', views.address_info, name='address_info'),
    
    # edit portfolio page
    path('edit_portfolio/', views.edit_portfolio, name='edit_portfolio'),
    
    # add wallet
    path('add_wallet/', views.add_wallet, name='add_wallet'),
    
    # delete user wallet
    path('user_wallets/del_wallet/<int:wallet_id>/', views.del_wallet, name='del_wallet'),
    
    # add address
    path('user_wallets/add_address/<int:wallet_id>/', views.add_address, name='add_address'),
    
    # delete address
    path('user_wallets/del_address/<int:address_id>/', views.del_address, name='del_address'),
    
    # page contains site info
    path('about/', views.about, name='about'),
    
    # page contains ours contacts
    path('contacts/', views.contacts, name='contacts'),
]
