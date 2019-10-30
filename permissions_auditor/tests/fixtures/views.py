"""Views used for testing."""
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import (
    login_required, permission_required, user_passes_test
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)
from django.utils.decorators import method_decorator
from django.views.generic import View


# Class Based Views


class BaseView(View):
    pass


class LoginRequiredView(LoginRequiredMixin, View):
    pass


class LoginRequiredMethodDecoratorView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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


class PermissionRequiredMethodDecoratorView(View):
    @method_decorator(permission_required('tests.test_perm'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class StaffMemberRequiredMethodDecoratorView(View):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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


# Function Based Views


def base_view(request):
    pass


@login_required
def login_required_view(request):
    pass


@permission_required('tests.test_perm')
def permission_required_view(request):
    pass


@permission_required(('tests.test_perm', 'tests.test_perm2'))
def permission_required_multi_view(request):
    pass


@staff_member_required
def staff_member_required_view(request):
    pass


@user_passes_test(lambda u: u.is_active)
def active_user_required_view(request):
    pass


@user_passes_test(lambda u: u.is_anonymous)
def anonymous_user_required_view(request):
    pass


@user_passes_test(lambda u: u.is_superuser)
def superuser_required_view(request):
    pass


@user_passes_test(lambda u: u.email is not None)
def user_passes_test_view(request):
    pass


@user_passes_test(lambda u: u.email is not None)
@login_required
def nested_decorator_view(request):
    pass
