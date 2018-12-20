from django.contrib.auth.views import LoginView
from django.urls import path

from .views import function_based

urlpatterns = [
    path('', function_based.home_page, name='home'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', function_based.logout_page, name='logout'),
    path('logout/done/', function_based.logged_out_page, name='logged_out'),

    path('users/', function_based.user_index, name='user_index'),

    path('permissions/', function_based.permissions_index, name='permissions_index'),
]
