from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render


class LoginPage(LoginView):
    template_name = 'admin/login.html'


class LogoutPage(LogoutView):
    next_page = 'home'


@login_required
def home_page(request):
    return render(request, 'home.html')
