"""Processors for class based views."""

import inspect

from .base import BaseCBVFileredProcessor


class PermissionRequiredMixinProcessor(BaseCBVFileredProcessor):
    class_filter = 'django.contrib.auth.mixins.PermissionRequiredMixin'

    def get_permission_required(self, view):
        return view().get_permission_required()

    def get_docstring(self, view):
        docstring = None

        # Check if has_permission has been overriden.
        if 'has_permission' in view.__dict__:
            docstring = inspect.getdoc(view.has_permission)

            if docstring is None or docstring.startswith('Override this method'):
                docstring = 'Custom (no docstring found)'

        return docstring


class LoginRequiredMixinProcessor(BaseCBVFileredProcessor):
    class_filter = 'django.contrib.auth.mixins.LoginRequiredMixin'

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        return 'Logged in user required'


class UserPassesTestMixinProcessor(BaseCBVFileredProcessor):
    class_filter = 'django.contrib.auth.mixins.UserPassesTestMixin'

    def get_docstring(self, view):
        docstring = inspect.getdoc(view().get_test_func())
        if docstring is None:
            docstring = 'Custom (no docstring found)'
        return docstring
