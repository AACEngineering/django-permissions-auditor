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

    def test_cb_baseview(self):
        self.assertProcessorResults(base_views.BaseView, can_process=False)

    def test_base_view(self):
        self.assertProcessorResults(base_views.base_view, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(mixin_views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(mixin_views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(mixin_views.UserPassesTestView, can_process=False)


class TestLoginRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.LoginRequiredDecoratorProcessor()

    def test_login_required_view(self):
        self.assertProcessorResults(
            views.login_required_view, can_process=True, login_required=True
        )

    def test_cb_loginrequired_decorator_view(self):
        self.assertProcessorResults(
            views.LoginRequiredMethodDecoratorView, can_process=True, login_required=True
        )

    def test_permission_required_view(self):
        self.assertProcessorResults(views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(views.staff_member_required_view, can_process=False)

    def test_staff_member_required_cb_view(self):
        self.assertProcessorResults(views.StaffMemberRequiredMethodDecoratorView, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(views.active_user_required_view, can_process=False)

    def test_active_user_required_cb_view(self):
        self.assertProcessorResults(
            views.ActiveUserRequiredMethodDecoratorView, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(views.anonymous_user_required_view, can_process=False)

    def test_anonymous_user_required_cb_view(self):
        self.assertProcessorResults(
            views.AnonymousUserRequiredMethodDecoratorView, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(views.superuser_required_view, can_process=False)

    def test_superuser_required_cb_view(self):
        self.assertProcessorResults(views.SuperUserRequiredMethodDecoratorView, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(views.user_passes_test_view, can_process=False)

    def test_nested_decorator_view(self):
        self.assertProcessorResults(
            views.nested_decorator_view, can_process=True, login_required=True
        )

    def test_nested_decorator_cb_view(self):
        self.assertProcessorResults(
            views.NestedMethodDecoratorView, can_process=True, login_required=True
        )


class TestPermissionRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.PermissionRequiredDecoratorProcessor()

    def test_login_required_view(self):
        self.assertProcessorResults(views.login_required_view, can_process=False)

    def test_cb_loginrequired_decorator_view(self):
        self.assertProcessorResults(views.LoginRequiredMethodDecoratorView, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            views.PermissionRequiredMethodDecoratorView,
            can_process=True, permissions=['tests.test_perm'], login_required=True
        )

    def test_cb_permission_required_view(self):
        self.assertProcessorResults(
            views.permission_required_view,
            can_process=True, permissions=['tests.test_perm'], login_required=True
        )

    def test_permission_required_multi_view(self):
        """Multiple permissions passed to @permission_required should be retrieved."""
        self.assertProcessorResults(
            views.permission_required_multi_view,
            can_process=True,
            permissions=['tests.test_perm', 'tests.test_perm2'], login_required=True,
        )

    def test_staff_member_required_view(self):
        self.assertProcessorResults(views.staff_member_required_view, can_process=False)

    def test_staff_member_required_cb_view(self):
        self.assertProcessorResults(views.StaffMemberRequiredMethodDecoratorView, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(views.active_user_required_view, can_process=False)

    def test_active_user_required_cb_view(self):
        self.assertProcessorResults(
            views.ActiveUserRequiredMethodDecoratorView, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(views.anonymous_user_required_view, can_process=False)

    def test_anonymous_user_required_cb_view(self):
        self.assertProcessorResults(
            views.AnonymousUserRequiredMethodDecoratorView, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(views.superuser_required_view, can_process=False)

    def test_superuser_required_cb_view(self):
        self.assertProcessorResults(views.SuperUserRequiredMethodDecoratorView, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(views.user_passes_test_view, can_process=False)

    def test_nested_decorator_view(self):
        self.assertProcessorResults(views.nested_decorator_view, can_process=False)


class StaffMemberRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.StaffMemberRequiredDecoratorProcessor()

    def test_login_required_view(self):
        self.assertProcessorResults(views.login_required_view, can_process=False)

    def test_cb_loginrequired_decorator_view(self):
        self.assertProcessorResults(views.LoginRequiredMethodDecoratorView, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(
            views.staff_member_required_view,
            can_process=True, login_required=True, docstring='Staff member required'
        )

    def test_staff_member_required_cb_view(self):
        self.assertProcessorResults(
            views.StaffMemberRequiredMethodDecoratorView,
            can_process=True, login_required=True, docstring='Staff member required'
        )

    def test_active_user_required_view(self):
        self.assertProcessorResults(views.active_user_required_view, can_process=False)

    def test_active_user_required_cb_view(self):
        self.assertProcessorResults(
            views.ActiveUserRequiredMethodDecoratorView, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(views.anonymous_user_required_view, can_process=False)

    def test_anonymous_user_required_cb_view(self):
        self.assertProcessorResults(
            views.AnonymousUserRequiredMethodDecoratorView, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(views.superuser_required_view, can_process=False)

    def test_superuser_required_cb_view(self):
        self.assertProcessorResults(views.SuperUserRequiredMethodDecoratorView, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(views.user_passes_test_view, can_process=False)

    def test_nested_decorator_view(self):
        self.assertProcessorResults(views.nested_decorator_view, can_process=False)


class ActiveUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.ActiveUserRequiredDecoratorProcessor()

    def test_login_required_view(self):
        self.assertProcessorResults(views.login_required_view, can_process=False)

    def test_cb_loginrequired_decorator_view(self):
        self.assertProcessorResults(views.LoginRequiredMethodDecoratorView, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        # Internally, ``staff_member_required`` runs this lamda:
        # lambda u: u.is_active and u.is_staff
        self.assertProcessorResults(
            views.staff_member_required_view,
            can_process=True, login_required=True, docstring='Active user required'
        )

    def test_staff_member_required_cb_view(self):
        # Quirk: when ``staf_member_required`` is wrapped with ``method_decorator``,
        # the lamda expression can no longer be found in the function closures,
        # so this should return false.
        self.assertProcessorResults(
            views.StaffMemberRequiredMethodDecoratorView, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(
            views.active_user_required_view,
            can_process=True, login_required=True, docstring='Active user required'
        )

    def test_active_user_required_cb_view(self):
        self.assertProcessorResults(
            views.ActiveUserRequiredMethodDecoratorView,
            can_process=True, login_required=True, docstring='Active user required'
        )

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(views.anonymous_user_required_view, can_process=False)

    def test_anonymous_user_required_cb_view(self):
        self.assertProcessorResults(
            views.AnonymousUserRequiredMethodDecoratorView, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(views.superuser_required_view, can_process=False)

    def test_superuser_required_cb_view(self):
        self.assertProcessorResults(views.SuperUserRequiredMethodDecoratorView, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(views.user_passes_test_view, can_process=False)

    def test_nested_decorator_view(self):
        self.assertProcessorResults(
            views.nested_decorator_view,
            can_process=True, login_required=True, docstring='Active user required'
        )

    def test_nested_decorator_cb_view(self):
        self.assertProcessorResults(
            views.NestedMethodDecoratorView,
            can_process=True, login_required=True, docstring='Active user required'
        )


class AnonymousUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.AnonymousUserRequiredDecoratorProcessor()

    def test_login_required_view(self):
        self.assertProcessorResults(views.login_required_view, can_process=False)

    def test_cb_loginrequired_decorator_view(self):
        self.assertProcessorResults(views.LoginRequiredMethodDecoratorView, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(views.staff_member_required_view, can_process=False)

    def test_staff_member_required_cb_view(self):
        self.assertProcessorResults(views.StaffMemberRequiredMethodDecoratorView, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(views.active_user_required_view, can_process=False)

    def test_active_user_required_cb_view(self):
        self.assertProcessorResults(
            views.ActiveUserRequiredMethodDecoratorView, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(
            views.anonymous_user_required_view,
            can_process=True, login_required=False, docstring='Anonymous user required'
        )

    def test_anonymous_user_required_cb_view(self):
        self.assertProcessorResults(
            views.AnonymousUserRequiredMethodDecoratorView,
            can_process=True, login_required=False, docstring='Anonymous user required'
        )

    def test_superuser_required_view(self):
        self.assertProcessorResults(views.superuser_required_view, can_process=False)

    def test_superuser_required_cb_view(self):
        self.assertProcessorResults(views.SuperUserRequiredMethodDecoratorView, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(views.user_passes_test_view, can_process=False)

    def test_nested_decorator_view(self):
        self.assertProcessorResults(views.nested_decorator_view, can_process=False)


class SuperUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.SuperUserRequiredDecoratorProcessor()

    def test_login_required_view(self):
        self.assertProcessorResults(views.login_required_view, can_process=False)

    def test_cb_loginrequired_decorator_view(self):
        self.assertProcessorResults(views.LoginRequiredMethodDecoratorView, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(views.staff_member_required_view, can_process=False)

    def test_staff_member_required_cb_view(self):
        self.assertProcessorResults(views.StaffMemberRequiredMethodDecoratorView, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(views.active_user_required_view, can_process=False)

    def test_active_user_required_cb_view(self):
        self.assertProcessorResults(views.ActiveUserRequiredMethodDecoratorView, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(views.anonymous_user_required_view, can_process=False)

    def test_anonymous_user_required_cb_view(self):
        self.assertProcessorResults(
            views.AnonymousUserRequiredMethodDecoratorView, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(
            views.superuser_required_view,
            can_process=True, login_required=True, docstring='Superuser required'
        )

    def test_superuser_required_cb_view(self):
        self.assertProcessorResults(
            views.SuperUserRequiredMethodDecoratorView,
            can_process=True, login_required=True, docstring='Superuser required'
        )

    def test_user_passes_test_view(self):
        self.assertProcessorResults(views.user_passes_test_view, can_process=False)

    def test_nested_decorator_view(self):
        self.assertProcessorResults(views.nested_decorator_view, can_process=False)


class UserPassesTestDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.UserPassesTestDecoratorProcessor()

    def test_login_required_view(self):
        self.assertProcessorResults(views.login_required_view, can_process=False)

    def test_cb_loginrequired_decorator_view(self):
        self.assertProcessorResults(views.LoginRequiredMethodDecoratorView, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(views.staff_member_required_view, can_process=False)

    def test_staff_member_required_cb_view(self):
        self.assertProcessorResults(views.StaffMemberRequiredMethodDecoratorView, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(views.active_user_required_view, can_process=False)

    def test_active_user_required_cb_view(self):
        self.assertProcessorResults(
            views.ActiveUserRequiredMethodDecoratorView, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(views.anonymous_user_required_view, can_process=False)

    def test_anonymous_user_required_cb_view(self):
        self.assertProcessorResults(
            views.AnonymousUserRequiredMethodDecoratorView, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(
            views.superuser_required_view, can_process=False)

    def test_superuser_required_cb_view(self):
        self.assertProcessorResults(views.SuperUserRequiredMethodDecoratorView, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(
            views.user_passes_test_view,
            can_process=True, login_required=None, docstring='Custom user test'
        )

    def test_user_passes_test_cb_view(self):
        self.assertProcessorResults(
            views.UserPassesTestMethodDecoratorView,
            can_process=True, login_required=None, docstring='Custom user test'
        )

    def test_nested_decorator_view(self):
        self.assertProcessorResults(
            views.nested_decorator_view,
            can_process=True, login_required=None, docstring='Custom user test'
        )

    def test_nested_decorator_cb_view(self):
        self.assertProcessorResults(
            views.NestedMethodDecoratorView,
            can_process=True, login_required=None, docstring='Custom user test'
        )
