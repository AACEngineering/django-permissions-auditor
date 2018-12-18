"""Processors for function based views."""

import inspect

from base import BaseFuncViewProcessor


class PermissionRequiredDecoratorProcessor(BaseFuncViewProcessor):

    def get_permission_required(self, view):
        permissions = []

        # Unwrap the function toget the permission passed through
        # the @permission_required() decorator.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).nonlocals
            if 'perm' in test_closures:
                perm = test_closures['perm']
                if isinstance(perm, str):
                    permissions.append(perm)
                else:
                    permissions.extend(perm)

        return permissions


class LoginRequiredDecoratorProcessor(BaseFuncViewProcessor):

    def get_login_required(self, view):
        # Unwrap the function and look for the @login_required() decorator.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if 'is_authenticated' in test_closures:
                return True

        return False
