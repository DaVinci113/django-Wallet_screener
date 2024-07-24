from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm


# Create your views here.


def register(request):
    """Регистрирует нового пользователя."""
    if request.method == 'POST':
        # Если форма верная
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            # Выполнение входа и перенаправление на домашнюю страницу.
            # login(request, new_user)
            return redirect('users:login')
    else:
        # Обработка заполненной формы.
        form = RegistrationForm()
    
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'users/register.html', context)
