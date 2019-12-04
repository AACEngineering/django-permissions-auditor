"""Processors for django auth decorators."""

import inspect

from .base import BaseDecoratorProcessor


class PermissionRequiredDecoratorProcessor(BaseDecoratorProcessor):
    """
    Process ``@permission_required()`` decorator.
    """

    def can_process(self, view):
        if inspect.isclass(view):
            for func in self._get_method_decorators(view.dispatch):
                if 'user_passes_test' not in (func.__name__, func.__qualname__.split('.')[0]):
                    continue

                test_func = inspect.getclosurevars(func).nonlocals['test_func']
                if test_func.__name__ == 'check_perms':
                    return True

        elif inspect.isfunction(view):
            # Unwrap the function and look for the has_perms property.
            return self._has_func_decorator(view, 'has_perms')

        return False

    def get_permission_required(self, view):
        permissions = []

        if inspect.isclass(view):
            for func in self._get_method_decorators(view.dispatch):
                if 'user_passes_test' not in (func.__name__, func.__qualname__.split('.')[0]):
                    continue

                test_func = inspect.getclosurevars(func).nonlocals['test_func']
                if test_func.__name__ == 'check_perms':
                    closures = inspect.getclosurevars(test_func).nonlocals
                    if 'perm' in closures:
                        perm = closures['perm']

                        # Ensure perm is not a function
                        if not inspect.isfunction(perm):
                            if isinstance(perm, str):
                                permissions.append(perm)
                            else:
                                permissions.extend(perm)

        elif inspect.isfunction(view) and self._has_test_func(view):
            for closure in self._get_test_func_closures(view):
                if 'perm' in closure.nonlocals:
                    perm = closure.nonlocals['perm']

                    # Ensure perm is not a function
                    if not inspect.isfunction(perm):
                        if isinstance(perm, str):
                            permissions.append(perm)
                        else:
                            permissions.extend(perm)

        return permissions

    def get_login_required(self, view):
        return True


class LoginRequiredDecoratorProcessor(BaseDecoratorProcessor):
    """
    Process ``@login_required`` decorator.
    """

    def can_process(self, view):
        if inspect.isclass(view):
            return self._has_method_decorator(view.dispatch, 'login_required')

        elif inspect.isfunction(view):
            # Unwrap the function and look for the is_authenticated property.
            return self._has_func_decorator(view, 'is_authenticated')

        return False

    def get_login_required(self, view):
        return True


class StaffMemberRequiredDecoratorProcessor(BaseDecoratorProcessor):
    """
    Process Django admin's ``@staff_member_required`` decorator.
    """

    def can_process(self, view):
        if inspect.isclass(view):
            return self._has_method_decorator(view.dispatch, 'staff_member_required')

        elif inspect.isfunction(view):
            # Unwrap the function and look for the is_staff property.
            return self._has_func_decorator(view, 'is_staff')

        return False

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        return 'Staff member required'


class ActiveUserRequiredDecoratorProcessor(BaseDecoratorProcessor):
    """
    Process ``@user_passes_test(lambda u: u.is_active)`` decorator.
    """

    def can_process(self, view):
        if inspect.isclass(view) and self._has_method_decorator(view.dispatch, 'user_passes_test'):
            return self._has_test_func_lambda(view.dispatch, 'is_active')

        elif inspect.isfunction(view):
            # Unwrap the function and look for the is_active property.
            return self._has_func_decorator(view, 'is_active')

        return False

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        return 'Active user required'


class AnonymousUserRequiredDecoratorProcessor(BaseDecoratorProcessor):
    """
    Process ``@user_passes_test(lambda u: u.is_anonymous)`` decorator.
    """

    def can_process(self, view):
        if inspect.isclass(view) and self._has_method_decorator(view.dispatch, 'user_passes_test'):
            return self._has_test_func_lambda(view.dispatch, 'is_anonymous')

        elif inspect.isfunction(view):
            # Unwrap the function and look for the is_anonymous property.
            return self._has_func_decorator(view, 'is_anonymous')

        return False

    def get_docstring(self, view):
        return 'Anonymous user required'


class SuperUserRequiredDecoratorProcessor(BaseDecoratorProcessor):
    """
    Process ``@user_passes_test(lambda u: u.is_superuser)`` decorator.
    """

    def can_process(self, view):
        if inspect.isclass(view) and self._has_method_decorator(view.dispatch, 'user_passes_test'):
            return self._has_test_func_lambda(view.dispatch, 'is_superuser')

        elif inspect.isfunction(view):
            # Unwrap the function and look for the is_superuser property.
            return self._has_func_decorator(view, 'is_superuser')

        return False

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        return 'Superuser required'


class UserPassesTestDecoratorProcessor(BaseDecoratorProcessor):
    """
    Process ``@user_passes_test()`` decorator.

    .. note::
        the ``@user_passes_test`` decorator does not automatically check
        that the User is not anonymous. This means they don't necessarily need
        to be authenticated for the check to pass, so this processor returns
        ``None`` (unknown) for the login_required attribute.
    """

    def can_process(self, view):
        # Some decorators use user_passes_test() internally, so we need to filter
        # them out since they are processed elsewhere.
        blacklist = (
            'is_authenticated', 'has_perms', 'is_staff', 'is_active', 'is_anonymous',
            'is_superuser',
        )

        if inspect.isclass(view):
            for func in self._get_method_decorators(view.dispatch):
                if 'user_passes_test' not in (func.__name__, func.__qualname__.split('.')[0]):
                    continue

                if not any([self._has_test_func_lambda(func, tag) for tag in blacklist]):
                    return True

        if inspect.isfunction(view) and self._has_test_func(view):
            for closure in self._get_test_func_closures(view):
                if not any([tag in closure.unbound for tag in blacklist]):
                    return True

        return False

    def get_login_required(self, view):
        return None

    def get_docstring(self, view):
        return 'Custom user test'
