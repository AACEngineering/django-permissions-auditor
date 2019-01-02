from permissions_auditor.core import get_all_views

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


@permission_required('auth.view_users')
def user_index(request):
    context = {
        'users': User.objects.filter(is_superuser=False)
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
