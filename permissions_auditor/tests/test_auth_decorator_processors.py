from django.contrib.auth.views import PasswordChangeView

from permissions_auditor.processors import auth_decorators
from permissions_auditor.tests.base import ProcessorTestCase
from permissions_auditor.tests.fixtures import (
    base_views, decorator_views as views, mixin_views
)


class DecoratorProcessorTestCaseMixin:
    """
    Decorator processors should not be able to process class based views
    that do not use ``@method_decorator``.
    """

    def test_cannot_process_non_method_decorator_cbvs(self):
        self.assertCannotProcess([
            base_views.BaseView, base_views.base_view,
            mixin_views.LoginRequiredView,
            mixin_views.PermissionRequiredView,
            mixin_views.UserPassesTestView
        ])


class TestLoginRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.LoginRequiredDecoratorProcessor()
        self.expected_results = {'login_required': True}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.permission_required_view, views.PermissionRequiredMethodDecoratorView,
            views.staff_member_required_view, views.StaffMemberRequiredMethodDecoratorView,
            views.active_user_required_view, views.ActiveUserRequiredMethodDecoratorView,
            views.anonymous_user_required_view, views.AnonymousUserRequiredMethodDecoratorView,
            views.superuser_required_view, views.SuperUserRequiredMethodDecoratorView,
            views.user_passes_test_view, views.UserPassesTestMethodDecoratorView
        ])

    def test_django_password_change_view(self):
        self.assertCanProcessView(PasswordChangeView, **self.expected_results)

    def test_login_required_view(self):
        self.assertCanProcessView(views.login_required_view, **self.expected_results)

    def test_cb_loginrequired_decorator_view(self):
        self.assertCanProcessView(views.LoginRequiredMethodDecoratorView, **self.expected_results)

    def test_nested_decorator_view(self):
        self.assertCanProcessView(views.nested_decorator_view, **self.expected_results)

    def test_nested_decorator_cbv(self):
        self.assertCanProcessView(views.NestedMethodDecoratorView, **self.expected_results)


class TestPermissionRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.PermissionRequiredDecoratorProcessor()
        self.expected_results = {'permissions': ['tests.test_perm'], 'login_required': True}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.login_required_view, views.LoginRequiredMethodDecoratorView,
            views.staff_member_required_view, views.StaffMemberRequiredMethodDecoratorView,
            views.active_user_required_view, views.ActiveUserRequiredMethodDecoratorView,
            views.anonymous_user_required_view, views.AnonymousUserRequiredMethodDecoratorView,
            views.superuser_required_view, views.SuperUserRequiredMethodDecoratorView,
            views.user_passes_test_view, views.UserPassesTestMethodDecoratorView,
            views.nested_decorator_view, views.NestedMethodDecoratorView
        ])

    def test_permission_required_view(self):
        self.assertCanProcessView(
            views.PermissionRequiredMethodDecoratorView, **self.expected_results
        )

    def test_permission_required_cbv(self):
        self.assertCanProcessView(views.permission_required_view, **self.expected_results)

    def test_permission_required_multi_view(self):
        """Multiple permissions passed to @permission_required should be retrieved."""
        self.assertCanProcessView(
            views.permission_required_multi_view,
            permissions=['tests.test_perm', 'tests.test_perm2'], login_required=True,
        )


class StaffMemberRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.StaffMemberRequiredDecoratorProcessor()
        self.expected_results = {'login_required': True, 'docstring': 'Staff member required'}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.login_required_view, views.LoginRequiredMethodDecoratorView,
            views.permission_required_view, views.PermissionRequiredMethodDecoratorView,
            views.active_user_required_view, views.ActiveUserRequiredMethodDecoratorView,
            views.anonymous_user_required_view, views.AnonymousUserRequiredMethodDecoratorView,
            views.superuser_required_view, views.SuperUserRequiredMethodDecoratorView,
            views.user_passes_test_view, views.UserPassesTestMethodDecoratorView,
            views.nested_decorator_view, views.NestedMethodDecoratorView
        ])

    def test_staff_member_required_view(self):
        self.assertCanProcessView(views.staff_member_required_view, **self.expected_results)

    def test_staff_member_required_cb_view(self):
        self.assertCanProcessView(
            views.StaffMemberRequiredMethodDecoratorView, **self.expected_results
        )


class ActiveUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.ActiveUserRequiredDecoratorProcessor()
        self.expected_results = {'login_required': True, 'docstring': 'Active user required'}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.login_required_view, views.LoginRequiredMethodDecoratorView,
            views.permission_required_view, views.PermissionRequiredMethodDecoratorView,
            views.anonymous_user_required_view, views.AnonymousUserRequiredMethodDecoratorView,
            views.superuser_required_view, views.SuperUserRequiredMethodDecoratorView,
            views.user_passes_test_view, views.UserPassesTestMethodDecoratorView
        ])

    def test_staff_member_required_view(self):
        # Internally, ``staff_member_required`` runs this lamda:
        # lambda u: u.is_active and u.is_staff
        self.assertCanProcessView(views.staff_member_required_view, **self.expected_results)

    def test_staff_member_required_cbv(self):
        # Quirk: when ``staf_member_required`` is wrapped with ``method_decorator``,
        # the lamda expression can no longer be found in the function closures,
        # so this should return false.
        self.assertCannotProcess([views.StaffMemberRequiredMethodDecoratorView])

    def test_active_user_required_view(self):
        self.assertCanProcessView(views.active_user_required_view, **self.expected_results)

    def test_active_user_required_cbv(self):
        self.assertCanProcessView(
            views.ActiveUserRequiredMethodDecoratorView, **self.expected_results
        )

    def test_nested_decorator_view(self):
        self.assertCanProcessView(views.nested_decorator_view, **self.expected_results)

    def test_nested_decorator_cbv(self):
        self.assertCanProcessView(views.NestedMethodDecoratorView, **self.expected_results)


class AnonymousUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.AnonymousUserRequiredDecoratorProcessor()
        self.expected_results = {'login_required': False, 'docstring': 'Anonymous user required'}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.login_required_view, views.LoginRequiredMethodDecoratorView,
            views.permission_required_view, views.PermissionRequiredMethodDecoratorView,
            views.staff_member_required_view, views.StaffMemberRequiredMethodDecoratorView,
            views.active_user_required_view, views.ActiveUserRequiredMethodDecoratorView,
            views.superuser_required_view, views.SuperUserRequiredMethodDecoratorView,
            views.user_passes_test_view, views.UserPassesTestMethodDecoratorView,
            views.nested_decorator_view, views.NestedMethodDecoratorView
        ])

    def test_anonymous_user_required_view(self):
        self.assertCanProcessView(views.anonymous_user_required_view, **self.expected_results)

    def test_anonymous_user_required_cbv(self):
        self.assertCanProcessView(
            views.AnonymousUserRequiredMethodDecoratorView, **self.expected_results
        )


class SuperUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.SuperUserRequiredDecoratorProcessor()
        self.expected_results = {'login_required': True, 'docstring': 'Superuser required'}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.login_required_view, views.LoginRequiredMethodDecoratorView,
            views.permission_required_view, views.PermissionRequiredMethodDecoratorView,
            views.staff_member_required_view, views.StaffMemberRequiredMethodDecoratorView,
            views.active_user_required_view, views.ActiveUserRequiredMethodDecoratorView,
            views.anonymous_user_required_view, views.AnonymousUserRequiredMethodDecoratorView,
            views.user_passes_test_view, views.UserPassesTestMethodDecoratorView,
            views.nested_decorator_view, views.NestedMethodDecoratorView
        ])

    def test_superuser_required_view(self):
        self.assertCanProcessView(views.superuser_required_view, **self.expected_results)

    def test_superuser_required_cbv(self):
        self.assertCanProcessView(
            views.SuperUserRequiredMethodDecoratorView, **self.expected_results
        )


class UserPassesTestDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.UserPassesTestDecoratorProcessor()
        self.expected_results = {'login_required': None, 'docstring': 'Custom user test'}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.login_required_view, views.LoginRequiredMethodDecoratorView,
            views.permission_required_view, views.PermissionRequiredMethodDecoratorView,
            views.staff_member_required_view, views.StaffMemberRequiredMethodDecoratorView,
            views.active_user_required_view, views.ActiveUserRequiredMethodDecoratorView,
            views.anonymous_user_required_view, views.AnonymousUserRequiredMethodDecoratorView,
            views.superuser_required_view, views.SuperUserRequiredMethodDecoratorView,
        ])

    def test_user_passes_test_view(self):
        self.assertCanProcessView(views.user_passes_test_view, **self.expected_results)

    def test_user_passes_test_cb_view(self):
        self.assertCanProcessView(views.UserPassesTestMethodDecoratorView, **self.expected_results)

    def test_nested_decorator_view(self):
        self.assertCanProcessView(views.nested_decorator_view, **self.expected_results)

    def test_nested_decorator_cbv(self):
        self.assertCanProcessView(views.NestedMethodDecoratorView, **self.expected_results)
