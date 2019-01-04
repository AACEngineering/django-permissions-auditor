from unittest.mock import patch

from django.conf import ImproperlyConfigured

from permissions_auditor.processors import base
from permissions_auditor.tests.base import ProcessorTestCase
from permissions_auditor.tests.fixtures import views


class BaseProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseProcessor()

    def test_process(self):
        self.assertProcessorResults(views.BaseView)


class BaseFuncViewProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseFuncViewProcessor()

    def test_can_process_class(self):
        self.assertProcessorResults(views.BaseView, can_process=False)

    def test_can_process_function(self):
        self.assertProcessorResults(views.base_view, can_process=True)


class BaseMixinProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseMixinProcessor()

    def test_can_process_class(self):
        self.assertProcessorResults(views.BaseView, can_process=True)

    def test_can_process_function(self):
        self.assertProcessorResults(views.base_view, can_process=False)


class BaseFilteredMixinProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseFileredMixinProcessor()

    def test_no_class_filter_raises_exception(self):
        with self.assertRaises(ImproperlyConfigured):
            self.assertProcessorResults(views.PermissionRequiredView)

    def test_can_process_filtered_class(self):
        self.processor.class_filter = 'django.contrib.auth.mixins.PermissionRequiredMixin'
        self.assertProcessorResults(views.PermissionRequiredView, can_process=True)
        self.assertProcessorResults(views.LoginRequiredView, can_process=False)

    def test_can_process_multiple_filtered_classses(self):
        self.processor.class_filter = (
            'django.contrib.auth.mixins.PermissionRequiredMixin',
            'django.contrib.auth.mixins.LoginRequiredMixin',
        )
        self.assertProcessorResults(views.PermissionRequiredView, can_process=True)
        self.assertProcessorResults(views.LoginRequiredView, can_process=True)

    def test_can_process_overriden_filtered_class(self):
        """
        can_process() should use use get_class_filter() if it is overridden.
        """
        self.processor.class_filter = None

        def filter_func(view):
            return ('django.contrib.auth.mixins.LoginRequiredMixin',)

        with patch.object(self.processor, 'get_class_filter', filter_func):
            self.assertProcessorResults(views.PermissionRequiredView, can_process=False)
            self.assertProcessorResults(views.LoginRequiredView, can_process=True)
