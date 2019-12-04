"""Views used for decorator testing."""
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import (
    login_required, permission_required, user_passes_test
)
from django.utils.decorators import method_decorator
from django.views.generic import View


@login_required
def login_required_view(request):
    pass


class LoginRequiredMethodDecoratorView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@permission_required('tests.test_perm')
def permission_required_view(request):
    pass


@permission_required(('tests.test_perm', 'tests.test_perm2'))
def permission_required_multi_view(request):
    pass


class PermissionRequiredMethodDecoratorView(View):
    @method_decorator(permission_required('tests.test_perm'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@staff_member_required
def staff_member_required_view(request):
    pass


class StaffMemberRequiredMethodDecoratorView(View):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_active)
def active_user_required_view(request):
    pass


class ActiveUserRequiredMethodDecoratorView(View):
    @method_decorator(user_passes_test(lambda u: u.is_active))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_anonymous)
def anonymous_user_required_view(request):
    pass


class AnonymousUserRequiredMethodDecoratorView(View):
    @method_decorator(user_passes_test(lambda u: u.is_anonymous))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def superuser_required_view(request):
    pass


class SuperUserRequiredMethodDecoratorView(View):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.email is not None)
def user_passes_test_view(request):
    pass


class UserPassesTestMethodDecoratorView(View):
    @method_decorator(user_passes_test(lambda u: u.email is not None))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@login_required
@user_passes_test(lambda u: u.is_active)
@user_passes_test(lambda u: u.email is not None)
def nested_decorator_view(request):
    pass


class NestedMethodDecoratorView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_active))
    @method_decorator(user_passes_test(lambda u: u.email is not None))
    def dispatch(self, request, *args, **kwargs):
        pass
