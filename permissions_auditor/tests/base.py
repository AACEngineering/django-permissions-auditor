from django.test import SimpleTestCase


class ProcessorTestCase(SimpleTestCase):
    processor = None

    def assertCannotProcess(self, views):
        for view in views:
            self.assertFalse(self.processor.can_process(view))

    def assertCanProcessView(self, view, permissions=[], login_required=False, docstring=None):
        self.assertTrue(self.processor.can_process(view))
        self.assertCountEqual(self.processor.get_permission_required(view), permissions)
        self.assertEqual(self.processor.get_login_required(view), login_required)
        self.assertEqual(self.processor.get_docstring(view), docstring)
