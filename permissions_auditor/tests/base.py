from django.test import SimpleTestCase


class ProcessorTestCase(SimpleTestCase):
    processor = None

    def assertProcessorResults(self, view,
                               can_process=True, permissions=[],
                               login_required=False, docstring=None):

        can_process_result = self.processor.can_process(view)
        self.assertEqual(can_process_result, can_process)

        if can_process_result:
            self.assertCountEqual(self.processor.get_permission_required(view), permissions)
            self.assertEqual(self.processor.get_login_required(view), login_required)
            self.assertEqual(self.processor.get_docstring(view), docstring)
