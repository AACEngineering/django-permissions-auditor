from permissions_auditor.processors import decorators
from permissions_auditor.tests import test_views
from permissions_auditor.tests.base import ProcessorTestCase


class TestLoginRequiredDecoratorProcessor(ProcessorTestCase):

    def setUp(self):
        self.processor = decorators.LoginRequiredDecoratorProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(test_views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(test_views.UserPassesTestView, can_process=False)

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(
            test_views.login_required_view,
            can_process=True,
            permissions=[],
            login_required=True,
            docstring='Logged in user required'
        )

    def test_permission_required_view(self):
        self.assertProcessorResults(test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class TestPermissionRequiredDecoratorProcessor(ProcessorTestCase):

    def setUp(self):
        self.processor = decorators.PermissionRequiredDecoratorProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(test_views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(test_views.UserPassesTestView, can_process=False)

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

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class StaffMemberRequiredDecoratorProcessor(ProcessorTestCase):

    def setUp(self):
        self.processor = decorators.StaffMemberRequiredDecoratorProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(test_views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(test_views.UserPassesTestView, can_process=False)

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
            docstring='Staff member required'
        )

    def test_superuser_required_view(self):
        self.assertProcessorResults(test_views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(test_views.user_passes_test_view, can_process=False)


class SuperUserRequiredDecoratorProcessor(ProcessorTestCase):

    def setUp(self):
        self.processor = decorators.SuperUserRequiredDecoratorProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(test_views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(test_views.UserPassesTestView, can_process=False)

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

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


class UserPassesTestDecoratorProcessor(ProcessorTestCase):

    def setUp(self):
        self.processor = decorators.UserPassesTestDecoratorProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(test_views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(test_views.UserPassesTestView, can_process=False)

    def test_base_view(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(test_views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(
            test_views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(test_views.staff_member_required_view, can_process=False)

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
