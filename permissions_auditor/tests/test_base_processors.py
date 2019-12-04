from unittest.mock import patch

from django.conf import ImproperlyConfigured

from permissions_auditor.processors import base
from permissions_auditor.tests.base import ProcessorTestCase
from permissions_auditor.tests.fixtures import views


class BaseProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseProcessor()

    def test_process(self):
        self.assertCanProcessView(views.BaseView)


class BaseFuncViewProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseFuncViewProcessor()

    def test_can_process_class(self):
        self.assertCannotProcess([views.BaseView])

    def test_can_process_function(self):
        self.assertCanProcessView(views.base_view)


class BaseCBVProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseCBVProcessor()

    def test_can_process_class(self):
        self.assertCanProcessView(views.BaseView)

    def test_can_process_function(self):
        self.assertCannotProcess([views.base_view])


class BaseFilteredMixinProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseFileredMixinProcessor()

    def test_no_class_filter_raises_exception(self):
        with self.assertRaises(ImproperlyConfigured):
            self.assertCannotProcess([views.PermissionRequiredView])

    def test_can_process_filtered_class(self):
        self.processor.class_filter = 'django.contrib.auth.mixins.PermissionRequiredMixin'
        self.assertCanProcessView(views.PermissionRequiredView)
        self.assertCannotProcess([views.LoginRequiredView])

    def test_can_process_multiple_filtered_classses(self):
        self.processor.class_filter = (
            'django.contrib.auth.mixins.PermissionRequiredMixin',
            'django.contrib.auth.mixins.LoginRequiredMixin',
        )
        self.assertCanProcessView(views.PermissionRequiredView)
        self.assertCanProcessView(views.LoginRequiredView)

    def test_can_process_overriden_filtered_class(self):
        """
        can_process() should use use get_class_filter() if it is overridden.
        """
        self.processor.class_filter = None

        def filter_func():
            return ('django.contrib.auth.mixins.LoginRequiredMixin',)

        with patch.object(self.processor, 'get_class_filter', filter_func):
            self.assertCannotProcess([views.PermissionRequiredView])
            self.assertCanProcessView(views.LoginRequiredView)
