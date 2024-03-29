
from django import VERSION as DJANGO_VERSION

if DJANGO_VERSION < (4, 0):
    # This can be removed once Django 3.2 and below support is dropped.
    from django.conf.urls import url, include as old_include

from django.urls import path, include, re_path

from . import views

new_style_urls = ([
    path('login_required/', views.login_required_view),
    re_path(r'^perm_required/$', views.permission_required_view),
], 'new_style_urls')

admin_namespace = ([
    path('staff_member_required/', views.staff_member_required_view),
], 'admin')

urlpatterns = [
    path('', views.BaseView.as_view()),
    path('multi_perm_view/', views.PermissionRequiredMultiView.as_view()),

    path('new_style/', include(new_style_urls)),
    path('admin/', include(admin_namespace)),
]

if DJANGO_VERSION < (4, 0):
    # This can be removed once Django 3.2 and below support is dropped.
    old_style_urls = ([
        url(r'^login_required/$', views.LoginRequiredView.as_view()),
        url(r'^perm_required/$', views.PermissionRequiredView.as_view()),
    ], 'old_style_urls')

    urlpatterns += [url('old_style/', old_include(old_style_urls))]
else:
    old_style_urls = ([
        re_path(r'^login_required/$', views.LoginRequiredView.as_view()),
        re_path(r'^perm_required/$', views.PermissionRequiredView.as_view()),
    ], 'old_style_urls')

    urlpatterns += [path('old_style/', include(old_style_urls))]
