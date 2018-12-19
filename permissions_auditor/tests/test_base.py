from unittest.mock import patch

from django.conf import ImproperlyConfigured

from permissions_auditor.processors import base
from permissions_auditor.tests import test_views
from permissions_auditor.tests.base import ProcessorTestCase


class BaseProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseProcessor()

    def test_process(self):
        self.assertProcessorResults(test_views.BaseView)


class BaseFuncViewProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseFuncViewProcessor()

    def test_can_process_class(self):
        self.assertProcessorResults(test_views.BaseView, can_process=False)

    def test_can_process_function(self):
        self.assertProcessorResults(test_views.base_view, can_process=True)


class BaseMixinProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseMixinProcessor()

    def test_can_process_class(self):
        self.assertProcessorResults(test_views.BaseView, can_process=True)

    def test_can_process_function(self):
        self.assertProcessorResults(test_views.base_view, can_process=False)


class BaseFilteredMixinProcessorTest(ProcessorTestCase):
    def setUp(self):
        self.processor = base.BaseFileredMixinProcessor()

    def test_no_class_filter_raises_exception(self):
        with self.assertRaises(ImproperlyConfigured):
            self.assertProcessorResults(test_views.PermissionRequiredView)

    def test_can_process_filtered_class(self):
        self.processor.class_filter = 'django.contrib.auth.mixins.PermissionRequiredMixin'
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=True)
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=False)

    def test_can_process_multiple_filtered_classses(self):
        self.processor.class_filter = (
            'django.contrib.auth.mixins.PermissionRequiredMixin',
            'django.contrib.auth.mixins.LoginRequiredMixin',
        )
        self.assertProcessorResults(test_views.PermissionRequiredView, can_process=True)
        self.assertProcessorResults(test_views.LoginRequiredView, can_process=True)

    def test_can_process_overriden_filtered_class(self):
        """
        can_process() should use use get_class_filter() if it is overrided.
        """
        self.processor.class_filter = None

        def filter_func(view):
            return ('django.contrib.auth.mixins.LoginRequiredMixin',)

        with patch.object(self.processor, 'get_class_filter', filter_func):
            self.assertProcessorResults(test_views.PermissionRequiredView, can_process=False)
            self.assertProcessorResults(test_views.LoginRequiredView, can_process=True)
