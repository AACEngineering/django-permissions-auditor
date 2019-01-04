from permissions_auditor.processors import auth_mixins
from permissions_auditor.tests.base import ProcessorTestCase
from permissions_auditor.tests.fixtures import views


class MixinProcessorTestCaseMixin:
    """Mixins should never be able to process function based views."""

    def test_base_view(self):
        self.assertProcessorResults(views.base_view, can_process=False)

    def test_login_required_view(self):
        self.assertProcessorResults(views.login_required_view, can_process=False)

    def test_permission_required_view(self):
        self.assertProcessorResults(views.permission_required_view, can_process=False)

    def test_staff_member_required_view(self):
        self.assertProcessorResults(views.staff_member_required_view, can_process=False)

    def test_active_user_required_view(self):
        self.assertProcessorResults(views.active_user_required_view, can_process=False)

    def test_anonymous_user_required_view(self):
        self.assertProcessorResults(views.anonymous_user_required_view, can_process=False)

    def test_superuser_required_view(self):
        self.assertProcessorResults(views.superuser_required_view, can_process=False)

    def test_user_passes_test_view(self):
        self.assertProcessorResults(views.user_passes_test_view, can_process=False)


class TestLoginRequiredMixinProcessor(MixinProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_mixins.LoginRequiredMixinProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(
            views.LoginRequiredView,
            can_process=True,
            permissions=[],
            login_required=True,
            docstring=None
        )

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(views.UserPassesTestView, can_process=False)


class TestPermissionRequiredMixinProcessor(MixinProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_mixins.PermissionRequiredMixinProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(views.LoginRequiredView, can_process=False)

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(
            views.PermissionRequiredView,
            can_process=True,
            permissions=['tests.test_perm'],
            login_required=True,
            docstring=None
        )

    def test_cb_permissionsrequiredview_docstring(self):
        """Views that implement has_permission() and have a docstring should be retrieved."""
        self.assertProcessorResults(
            views.PermissionRequiredViewDocstring,
            can_process=True,
            permissions=['tests.test_perm'],
            login_required=True,
            docstring='Custom docstrings should be detected.'
        )

    def test_cb_permissionsrequiredview_no_docstring(self):
        """
        Views that implement has_permission() and do not have a docstring
        should return a default messsage.
        """
        self.assertProcessorResults(
            views.PermissionRequiredViewNoDocstring,
            can_process=True,
            permissions=['tests.test_perm'],
            login_required=True,
            docstring='Custom (no docstring found)'
        )

    def test_cb_permissionrequiredview_multi(self):
        """
        Views with multiple permissions should return all permissions.
        """
        self.assertProcessorResults(
            views.PermissionRequiredMultiView,
            can_process=True,
            permissions=['tests.test_perm', 'tests.test_perm2'],
            login_required=True,
            docstring=None
        )

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(views.UserPassesTestView, can_process=False)


class TestUserPassesTestMixinProcessor(MixinProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_mixins.UserPassesTestMixinProcessor()

    def test_cb_baseview(self):
        self.assertProcessorResults(views.BaseView, can_process=False)

    def test_cb_loginrequiredview(self):
        self.assertProcessorResults(views.LoginRequiredView, can_process=False)

    def test_cb_userpassestestview(self):
        self.assertProcessorResults(
            views.UserPassesTestView,
            can_process=True,
            permissions=[],
            login_required=None,
            docstring='Custom (no docstring found)'
        )

    def test_cb_permissionsrequiredview(self):
        self.assertProcessorResults(views.PermissionRequiredView, can_process=False)

    def test_cb_userpassestestview_docstring(self):
        """Views that implement test_func() and have a docstring should be retrieved."""
        self.assertProcessorResults(
            views.UserPassesTestViewDocstring,
            can_process=True,
            permissions=[],
            login_required=None,
            docstring='Custom docstrings should be detected.'
        )

    def test_cb_userpassestestview_no_docstring(self):
        """
        Views that implement test_func() and do not have a docstring
        should return a default messsage.
        """
        self.assertProcessorResults(
            views.UserPassesTestViewNoDocstring,
            can_process=True,
            permissions=[],
            login_required=None,
            docstring='Custom (no docstring found)'
        )

    def test_cb_userpassestestview_custom_func(self):
        """
        Views that override get_test_func() should check the new function returned
        instead of the default test_func() function.
        """
        self.assertProcessorResults(
            views.UserPassesTestViewCustomFunc,
            can_process=True,
            permissions=[],
            login_required=None,
            docstring='Custom docstrings should be detected.'
        )
