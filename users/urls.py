from django.urls import path, include

app_name = 'users'
urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
]
