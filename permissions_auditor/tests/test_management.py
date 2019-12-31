from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class CheckViewPermsTest(TestCase):

    def test_missing_perms(self):
        out = StringIO()
        call_command('check_view_permissions', stdout=out)
        self.assertIn('`tests.test_perm`', out.getvalue())
        self.assertIn('`tests.test_perm2`', out.getvalue())
