from permissions_auditor.core import get_views

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

User = get_user_model()


class UserIndex(PermissionRequiredMixin, TemplateView):
    template_name = 'users.html'
    permission_required = 'auth.view_user'

    def has_permission(self):
        """PermissionRequiredMixin - Docstrings on `has_permission()` are displayed in the admin."""
        return super().has_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_superuser=False)
        return context


class SuperUserIndex(UserPassesTestMixin, TemplateView):
    template_name = 'users.html'
    permission_required = 'auth.view_user'

    def test_func(self):
        """UserPassesTestMixin - The user must be a superuser to access."""
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_superuser=True)
        return context


class PermissionsIndex(PermissionRequiredMixin, TemplateView):
    template_name = 'permissions_list.html'
    permission_required = ('auth.view_user', 'auth.change_user',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['views'] = get_views()
        return context
