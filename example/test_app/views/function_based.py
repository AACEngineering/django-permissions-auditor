from permissions_auditor.core import get_all_views

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import (
    login_required, permission_required, user_passes_test
)
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

User = get_user_model()


def home_page(request):
    return render(request, 'home.html')


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('logged_out'))


@user_passes_test(lambda u: not u.is_authenticated)
def logged_out_page(request):
    return render(request, 'registration/logged_out.html')


@permission_required('auth.view_users')
def user_index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def superuser_index(request):
    context = {
        'users': User.objects.filter(is_superuser=True)
    }
    return render(request, 'users.html', context)


@staff_member_required
def permissions_index(request):
    context = {
        'views': get_all_views()
    }
    return render(request, 'permissions_list.html', context)
