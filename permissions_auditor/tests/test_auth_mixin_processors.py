from permissions_auditor.processors import auth_mixins
from permissions_auditor.tests.base import ProcessorTestCase
from permissions_auditor.tests.fixtures import views


class MixinProcessorTestCaseMixin:
    """Mixins should never be able to process function based views."""

    def assert_cannot_process_non_cbvs(self):
        self.assertCannotProcess([
            views.base_view, views.BaseView,
            views.login_required_view,
            views.staff_member_required_view,
            views.active_user_required_view,
            views.anonymous_user_required_view,
            views.superuser_required_view,
            views.user_passes_test_view
        ])


class TestLoginRequiredMixinProcessor(MixinProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_mixins.LoginRequiredMixinProcessor()
        self.expected_results = {'permissions': [], 'login_required': True, 'docstring': None}

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.PermissionRequiredView, views.PermissionRequiredMultiView,
            views.PermissionRequiredViewNoPerm,
            views.PermissionRequiredViewDocstring, views.PermissionRequiredViewNoDocstring,
            views.UserPassesTestView, views.UserPassesTestViewCustomFunc,
            views.UserPassesTestViewDocstring, views.UserPassesTestViewNoDocstring
        ])

    def test_cb_loginrequiredview(self):
        self.assertCanProcessView(views.LoginRequiredView, **self.expected_results)


class TestPermissionRequiredMixinProcessor(MixinProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_mixins.PermissionRequiredMixinProcessor()

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.LoginRequiredView,
            views.UserPassesTestView, views.UserPassesTestViewCustomFunc,
            views.UserPassesTestViewDocstring, views.UserPassesTestViewNoDocstring
        ])

    def test_cb_permissionsrequiredview(self):
        self.assertCanProcessView(
            views.PermissionRequiredView,
            permissions=['tests.test_perm'], login_required=True, docstring=None
        )

    def test_cb_permissionsrequiredview_no_perm(self):
        """
        Views that override has_permission() and do not set permission_required should be processed.
        """
        self.assertCanProcessView(
            views.PermissionRequiredViewNoPerm,
            permissions=[], login_required=True, docstring='The user\'s first name must be Bob'
        )

    def test_cb_permissionsrequiredview_docstring(self):
        """Views that implement has_permission() and have a docstring should be retrieved."""
        self.assertCanProcessView(
            views.PermissionRequiredViewDocstring,
            permissions=['tests.test_perm'], login_required=True,
            docstring='Custom docstrings should be detected.'
        )

    def test_cb_permissionsrequiredview_no_docstring(self):
        """
        Views that implement has_permission() and do not have a docstring
        should return a default messsage.
        """
        self.assertCanProcessView(
            views.PermissionRequiredViewNoDocstring,
            permissions=['tests.test_perm'], login_required=True,
            docstring='Custom (no docstring found)'
        )

    def test_cb_permissionrequiredview_multi(self):
        """
        Views with multiple permissions should return all permissions.
        """
        self.assertCanProcessView(
            views.PermissionRequiredMultiView,
            permissions=['tests.test_perm', 'tests.test_perm2'], login_required=True, docstring=None
        )


class TestUserPassesTestMixinProcessor(MixinProcessorTestCaseMixin, ProcessorTestCase):

    def setUp(self):
        self.processor = auth_mixins.UserPassesTestMixinProcessor()

    def test_cannot_process(self):
        self.assertCannotProcess([
            views.LoginRequiredView,
            views.PermissionRequiredView, views.PermissionRequiredMultiView,
            views.PermissionRequiredViewNoPerm,
            views.PermissionRequiredViewDocstring, views.PermissionRequiredViewNoDocstring
        ])

    def test_cb_userpassestestview(self):
        self.assertCanProcessView(
            views.UserPassesTestView,
            permissions=[], login_required=None, docstring='Custom (no docstring found)'
        )

    def test_cb_userpassestestview_docstring(self):
        """Views that implement test_func() and have a docstring should be retrieved."""
        self.assertCanProcessView(
            views.UserPassesTestViewDocstring,
            permissions=[], login_required=None, docstring='Custom docstrings should be detected.'
        )

    def test_cb_userpassestestview_no_docstring(self):
        """
        Views that implement test_func() and do not have a docstring
        should return a default messsage.
        """
        self.assertCanProcessView(
            views.UserPassesTestViewNoDocstring,
            permissions=[], login_required=None, docstring='Custom (no docstring found)'
        )

    def test_cb_userpassestestview_custom_func(self):
        """
        Views that override get_test_func() should check the new function returned
        instead of the default test_func() function.
        """
        self.assertCanProcessView(
            views.UserPassesTestViewCustomFunc,
            permissions=[], login_required=None, docstring='Custom docstrings should be detected.'
        )
