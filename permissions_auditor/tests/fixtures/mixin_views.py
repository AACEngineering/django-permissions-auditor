"""Views used for testing."""
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)
from django.views.generic import View


class LoginRequiredView(LoginRequiredMixin, View):
    pass


class PermissionRequiredView(PermissionRequiredMixin, View):
    permission_required = 'tests.test_perm'


class PermissionRequiredMultiView(PermissionRequiredMixin, View):
    permission_required = ('tests.test_perm', 'tests.test_perm2')


class PermissionRequiredViewNoPerm(PermissionRequiredMixin, View):

    def has_permission(self):
        """The user's first name must be Bob"""
        return self.request.user.first_name == 'Bob'


class PermissionRequiredViewDocstring(PermissionRequiredMixin, View):
    permission_required = 'tests.test_perm'

    def has_permission(self):
        """Custom docstrings should be detected."""
        return super().has_permission()


class PermissionRequiredViewNoDocstring(PermissionRequiredMixin, View):
    permission_required = 'tests.test_perm'

    def has_permission(self):
        return super().has_permission()


class UserPassesTestView(UserPassesTestMixin, View):
    def test_func(self):
        return True


class UserPassesTestViewDocstring(UserPassesTestMixin, View):
    def test_func(self):
        """Custom docstrings should be detected."""
        return True


class UserPassesTestViewNoDocstring(UserPassesTestMixin, View):
    def test_func(self):
        return True


class UserPassesTestViewCustomFunc(UserPassesTestMixin, View):
    def get_test_func(self):
        return self.custom_test_func

    def custom_test_func(self):
        """Custom docstrings should be detected."""
        return True
