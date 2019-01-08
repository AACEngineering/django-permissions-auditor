"""Processors for django auth mixins."""

import inspect

from django.conf import ImproperlyConfigured

from .base import BaseFileredMixinProcessor


class PermissionRequiredMixinProcessor(BaseFileredMixinProcessor):
    """
    Processes views that directly inherit from
    ``django.contrib.auth.mixins.PermissionRequiredMixin``.

    .. hint::
        If the ``has_permission()`` function is overridden, any docstrings on that
        function will be displayed in the additional info column.
    """

    class_filter = 'django.contrib.auth.mixins.PermissionRequiredMixin'

    def get_permission_required(self, view):
        try:
            return view().get_permission_required()
        except ImproperlyConfigured:
            return []

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        docstring = None

        # Check if has_permission has been overriden.
        if 'has_permission' in view.__dict__:
            docstring = inspect.getdoc(view.has_permission)

            if docstring is None or docstring.startswith('Override this method'):
                docstring = 'Custom (no docstring found)'

        return docstring


class LoginRequiredMixinProcessor(BaseFileredMixinProcessor):
    """
    Processes views that directly inherit from
    ``django.contrib.auth.mixins.LoginRequiredMixin``.
    """

    class_filter = 'django.contrib.auth.mixins.LoginRequiredMixin'

    def get_login_required(self, view):
        return True


class UserPassesTestMixinProcessor(BaseFileredMixinProcessor):
    """
    Processes views that directly inherit from
    ``django.contrib.auth.mixins.UserPassesTestMixin``.

    .. hint::
        If the function returned by ``get_test_func()`` is overridden, any docstrings
        on that function will be displayed in the additional info column.

    .. note::
        UserPassesTestMixinProcessor does not automatically check
        that the User is not anonymous. This means they don't necessarily need
        to be authenticated for the check to pass, so this processor returns
        ``None`` (unknown) for the login_required attribute.
    """

    class_filter = 'django.contrib.auth.mixins.UserPassesTestMixin'

    def get_login_required(self, view):
        return None

    def get_docstring(self, view):
        docstring = inspect.getdoc(view().get_test_func())
        if docstring is None:
            docstring = 'Custom (no docstring found)'
        return docstring
