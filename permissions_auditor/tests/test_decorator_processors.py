from permissions_auditor.processors import auth_decorators
from permissions_auditor.tests import test_views
from permissions_auditor.tests.base import ProcessorTestCase


class DecoratorProcessorTestCaseMixin:
    """Decorators should never be able to process class based views."""

    def test_cb_baseview(self):
        self.assertProcessorResults(test_views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(test_views.UserPassesTestView, can_process=False)


class TestLoginRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.LoginRequiredDecoratorProcessor()

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(
            test_views.login_required_view,
            can_process=True,
            permissions=[],
            login_required=True,
            docstring=None
        )

    def test_permission_required_view(self):
        self.assertProcessorResults(test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(test_views.active_user_required_view, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(test_views.anonymous_user_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class TestPermissionRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.PermissionRequiredDecoratorProcessor()

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            test_views.permission_required_view,
            can_process=True,
            permissions=['tests.test_perm'],
            login_required=True,
            docstring=None
        )

    def test_permission_required_multi_view(self):
        """Multiple permissions passed to @permission_required should be retrieved."""
        self.assertProcessorResults(
            test_views.permission_required_multi_view,
            can_process=True,
            permissions=['tests.test_perm', 'tests.test_perm2'],
            login_required=True,
            docstring=None
        )

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(test_views.active_user_required_view, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(test_views.anonymous_user_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class StaffMemberRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.StaffMemberRequiredDecoratorProcessor()

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(
            test_views.staff_member_required_view,
            can_process=True,
            permissions=[],
            login_required=True,
            docstring='Staff member required'
        )

    def test_active_user_required_view(self):
        self.assertProcessorResults(test_views.active_user_required_view, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(test_views.anonymous_user_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class ActiveUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.ActiveUserRequiredDecoratorProcessor()

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(
            test_views.staff_member_required_view,
            can_process=True,
            permissions=[],
            login_required=True,
            docstring='Active user required'
        )

    def test_active_user_required_view(self):
        self.assertProcessorResults(
            test_views.active_user_required_view,
            can_process=True,
            permissions=[],
            login_required=True,
            docstring='Active user required'
        )

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(test_views.anonymous_user_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class AnonymousUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.AnonymousUserRequiredDecoratorProcessor()

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(test_views.active_user_required_view, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(
            test_views.anonymous_user_required_view,
            can_process=True,
            permissions=[],
            login_required=False,
            docstring='Anonymous user required'
        )

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class SuperUserRequiredDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.SuperUserRequiredDecoratorProcessor()

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(test_views.active_user_required_view, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(test_views.anonymous_user_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(
            test_views.superuser_required_view,
            can_process=True,
            permissions=[],
            login_required=True,
            docstring='Superuser required'
        )

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class UserPassesTestDecoratorProcessor(DecoratorProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_decorators.UserPassesTestDecoratorProcessor()

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(test_views.active_user_required_view, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(test_views.anonymous_user_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(
            test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(
            test_views.user_passes_test_view,
            can_process=True,
            permissions=[],
            login_required=False,
            docstring='Custom user test'
        )
