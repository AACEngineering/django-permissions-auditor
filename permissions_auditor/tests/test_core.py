from django.conf import ImproperlyConfigured
from django.test import SimpleTestCase

from permissions_auditor import core
from permissions_auditor.core import ViewDetails
from permissions_auditor.tests.fixtures import views


class ViewParserTest(SimpleTestCase):

    def setUp(self):
        self.parser = core.ViewParser()

    def test_invalid_config(self):
        """
        Invalid processors should raise ImproperlyConfigured.
        """
        with self.settings(PERMISSIONS_AUDITOR_PROCESSORS=['invalid_parser']):
            self.assertRaises(ImproperlyConfigured, lambda: core.ViewParser())

    def test_no_parsers(self):
        with self.settings(PERMISSIONS_AUDITOR_PROCESSORS=[]):
            parser = core.ViewParser()
            results = parser.parse(views.LoginRequiredView)
            self.assertEqual(results, ([], False, ''))

    def test_parse_cbv(self):
        """
        The default configuration should be able to parse PermissionRequiredMixin.
        """
        results = self.parser.parse(views.PermissionRequiredViewDocstring)
        self.assertEqual(
            results, (['tests.test_perm'], True, 'Custom docstrings should be detected.')
        )

    def test_parse_func_view(self):
        """
        The default configuration should be able to parse @permission_required().
        """
        results = self.parser.parse(views.permission_required_view)
        self.assertEqual(
            results, (['tests.test_perm'], True, '')
        )


class GetViewsTest(SimpleTestCase):

    def setUp(self):
        self.module = 'permissions_auditor.tests.fixtures.views'
        self.views_results = [
            ViewDetails(
                module=self.module, name='BaseView',
                url='/',
                permissions=[], login_required=False, docstring=''
            ),
            ViewDetails(
                module=self.module, name='PermissionRequiredMultiView',
                url='/multi_perm_view/',
                permissions=['tests.test_perm', 'tests.test_perm2'],
                login_required=True, docstring=''
            ),
            ViewDetails(
                module=self.module, name='login_required_view',
                url='/new_style/login_required/',
                permissions=[], login_required=True, docstring=''
            ),
            ViewDetails(
                module=self.module, name='permission_required_view',
                url='/new_style/perm_required/',
                permissions=['tests.test_perm'], login_required=True, docstring=''
            ),
            ViewDetails(
                module=self.module, name='staff_member_required_view',
                url='/admin/staff_member_required/',
                permissions=[], login_required=True, docstring='Staff member required'
            ),
            ViewDetails(
                module=self.module, name='LoginRequiredView',
                url='/old_style/login_required/',
                permissions=[], login_required=True, docstring=''
            ),
            ViewDetails(
                module=self.module, name='PermissionRequiredView',
                url='/old_style/perm_required/',
                permissions=['tests.test_perm'], login_required=True, docstring=''
            ),
        ]

    def reload_blacklist(self):
        """
        The blacklist is loaded when the app starts, we need to override the values
        when we change settings.
        """
        core.NAMESPACE_BLACKLIST = tuple(core._get_blacklist('namespaces'))
        core.VIEW_BLACKLIST = tuple(core._get_blacklist('view_names'))
        core.MODULE_BLACKLIST = tuple(core._get_blacklist('modules'))

    def test_get_views_results(self):
        blacklist = {
            'namespaces': [],
            'view_names': [],
            'modules': [],
        }

        with self.settings(PERMISSIONS_AUDITOR_BLACKLIST=blacklist):
            self.reload_blacklist()
            views = core.get_views()
            self.assertSequenceEqual(views, self.views_results)

    def test_namespace_blacklist(self):
        blacklist = {
            'namespaces': ['admin'],
            'view_names': [],
            'modules': [],
        }

        with self.settings(PERMISSIONS_AUDITOR_BLACKLIST=blacklist):
            self.reload_blacklist()
            views = core.get_views()
            self.assertNotIn(views, self.views_results[3])  # staff_member_required_view

    def test_view_name_blacklist(self):
        blacklist = {
            'namespaces': [],
            'view_names': ['{}.BaseView'.format(self.module)],
            'modules': [],
        }

        with self.settings(PERMISSIONS_AUDITOR_BLACKLIST=blacklist):
            self.reload_blacklist()
            views = core.get_views()
            self.assertNotIn(views, self.views_results[0])  # BaseView

    def test_module_blacklist(self):
        blacklist = {
            'namespaces': [],
            'view_names': [],
            'modules': [self.module],
        }

        with self.settings(PERMISSIONS_AUDITOR_BLACKLIST=blacklist):
            self.reload_blacklist()
            views = core.get_views()
            self.assertEqual(views, [])
