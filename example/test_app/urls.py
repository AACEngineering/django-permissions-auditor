from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include

from test_app import views
from test_app.views import cbv_based, function_based

cbv_namespace = ([
    path('users/', cbv_based.UserIndex.as_view(), name='user_index'),
    path('super_users/', cbv_based.SuperUserIndex.as_view(), name='superuser_index'),
    path('permissions/', cbv_based.PermissionsIndex.as_view(), name='permissions_index'),
], 'cbv')

func_namespaces = ([
    path('users/', function_based.user_index, name='user_index'),
    path('super_users/', function_based.superuser_index, name='superuser_index'),
    path('permissions/', function_based.permissions_index, name='permissions_index'),
    path('invalid/', function_based.invalid_permission_view, name='invalid_permission_view'),
], 'func')

urlpatterns = [
    path('', views.home_page, name='home'),

    path('accounts/login/', views.LoginPage.as_view(), name='login'),
    path('accounts/logout/', views.LogoutPage.as_view(), name='logout'),
    path('accounts/password/change/', PasswordChangeView.as_view(), name='change_password'),

    path('cbv/', include(cbv_namespace)),
    path('func/', include(func_namespaces)),
]
