"""Processors for django auth decorators."""

import inspect

from .base import BaseFuncViewProcessor


class PermissionRequiredDecoratorProcessor(BaseFuncViewProcessor):

    def can_process(self, view):
        if not super().can_process(view):
            return False

        # Unwrap the function and look for the has_perms() function.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if 'has_perms' in test_closures:
                return True

        return False

    def get_permission_required(self, view):
        permissions = []

        # Unwrap the function and search for the permission passed through
        # the @permission_required() decorator.
        closures = inspect.getclosurevars(view).nonlocals['test_func']
        test_func_closures = inspect.getclosurevars(closures).nonlocals
        if 'perm' in test_func_closures:
            perm = test_func_closures['perm']

            # Ensure perm is not a function
            if not inspect.isfunction(perm):
                if isinstance(perm, str):
                    permissions.append(perm)
                else:
                    permissions.extend(perm)

        return permissions

    def get_login_required(self, view):
        return True


class LoginRequiredDecoratorProcessor(BaseFuncViewProcessor):

    def can_process(self, view):
        if not super().can_process(view):
            return False

        # Unwrap the function and look for the is_authenticated property.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if 'is_authenticated' in test_closures:
                return True

        return False

    def get_login_required(self, view):
        return True


class StaffMemberRequiredDecoratorProcessor(BaseFuncViewProcessor):

    def can_process(self, view):
        if not super().can_process(view):
            return False

        # Unwrap the function and look for the is_staff property.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if 'is_staff' in test_closures:
                return True

        return False

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        return 'Staff member required'


class ActiveUserRequiredDecoratorProcessor(BaseFuncViewProcessor):
    """
    This isn't an actual decorator, but is common enough to merit a processor.

    It detects this:

    @user_passes_test(lambda u: u.is_active)


    Note that this processor will process the @staff_member_required decorator
    since it includes an is_active check.
    """

    def can_process(self, view):
        if not super().can_process(view):
            return False

        # Unwrap the function and look for the is_active property.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if 'is_active' in test_closures:
                return True

        return False

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        return 'Active user required'


class AnonymousUserRequiredDecoratorProcessor(BaseFuncViewProcessor):
    """
    This isn't an actual decorator, but is common enough to merit a processor.

    It detects this:

    @user_passes_test(lambda u: u.is_anonymous)
    """

    def can_process(self, view):
        if not super().can_process(view):
            return False

        # Unwrap the function and look for the is_anonymous property.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if 'is_anonymous' in test_closures:
                return True

        return False

    def get_docstring(self, view):
        return 'Anonymous user required'


class SuperUserRequiredDecoratorProcessor(BaseFuncViewProcessor):
    """
    This isn't an actual decorator, but is common enough to merit a processor.

    It detects this:

    @user_passes_test(lambda u: u.is_superuser)
    """

    def can_process(self, view):
        if not super().can_process(view):
            return False

        # Unwrap the function and look for the is_superuser property.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if 'is_superuser' in test_closures:
                return True

        return False

    def get_login_required(self, view):
        return True

    def get_docstring(self, view):
        return 'Superuser required'


class UserPassesTestDecoratorProcessor(BaseFuncViewProcessor):
    """
    Note: the user_passes_test decorator does not automatically check
    that the User is not anonymous. This means they don't necessarily need
    to be authenticated for the check to pass.
    """

    def can_process(self, view):
        if not super().can_process(view):
            return False

        # The other decorators build from the user_passes_test decorator,
        # so we need to blacklist their functions so we don't override their results.
        blacklist = (
            'is_authenticated', 'has_perms', 'is_staff', 'is_active', 'is_anonymous',
            'is_superuser',
        )

        # Unwrap the function and look for any test functions inside the decorator.
        closures = inspect.getclosurevars(view).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            return any([closure not in blacklist for closure in test_closures])

        return False

    def get_docstring(self, view):
        return 'Custom user test'
