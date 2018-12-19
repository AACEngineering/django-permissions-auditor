from django.contrib.auth import logout
from django.contrib.auth.decorators import (
    login_required, user_passes_test
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html')


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('logged_out'))


@user_passes_test(lambda u: not u.is_authenticated)
def logged_out_page(request):
    return render(request, 'registration/logged_out.html')
