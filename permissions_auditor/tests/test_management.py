from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class CheckViewPermsTest(TestCase):

    def test_missing_perms(self):
        out = StringIO()
        call_command('check_view_permissions', stdout=out)
        self.assertIn('`tests.test_perm`', out.getvalue())
        self.assertIn('`tests.test_perm2`', out.getvalue())


class CheckDumpViewPermsTest(TestCase):

    def test_dump_perms_no_args(self):
        out = StringIO()
        call_command('dump_view_permissions', stdout=out)

        # Default output should be JSON formatted
        self.assertIn('[{"module": "permissions_auditor.tests.fixtures.views"', out.getvalue())

    def test_dump_perms_json(self):
        out = StringIO()
        call_command('dump_view_permissions', format='json', stdout=out)

        # Output should be JSON formatted
        self.assertIn('[{"module": "permissions_auditor.tests.fixtures.views"', out.getvalue())

    def test_dump_perms_csv(self):
        out = StringIO()
        call_command('dump_view_permissions', format='csv', stdout=out)

        # CSV output header should be present
        self.assertIn('module,name,url,permissions,login_required,docstring', out.getvalue())
