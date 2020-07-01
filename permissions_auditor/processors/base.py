import inspect

from django.conf import ImproperlyConfigured


class BaseProcessor:

    def can_process(self, view):
        """
        Can this processor process the provided view?

        :param view: the view being processed.
        :type view: function or class
        :return: whether this processor can process the view.
                 Default: ``False``
        :rtype: boolean
        """
        return True

    def get_permission_required(self, view):
        """
        Returns permissions required on the provided view.
        Must return an iterable.

        :param view: the view being processed.
        :type view: function or class
        :return: the permissions required to access the view. Default: ``[]``
        :rtype: list(str)
        """
        return []

    def get_login_required(self, view):
        """
        Returns if a user needs to be logged in to access the view.

        :param view: the view being processed.
        :type view: function or class
        :return: whether a user must be logged in to access this view.
                 Default: ``False``
        :rtype: boolean or None (if unknown)
        """
        return False

    def get_docstring(self, view):
        """
        Returns any additional information that should be displayed when
        showing permisison information.

        :param view: the view being processed.
        :type view: function or class
        :return: the string to display in the additional info column. Default: ``None``
        :rtype: str or None
        """
        return None


class BaseFuncViewProcessor(BaseProcessor):
    """Base class for processing function based views."""

    def can_process(self, view):
        return inspect.isfunction(view)


class BaseCBVProcessor(BaseProcessor):
    """Base class for processing class based views."""

    def can_process(self, view):
        return inspect.isclass(view)


class BaseDecoratorProcessor(BaseProcessor):
    """Base class with utilities for unwrapping decorators."""

    def _has_method_decorator(self, function, func_name):
        """
        Checks if a function with the name `func_name` (str) is present within the
        ``@method_decorator`` on the provided function.
        """
        closures = inspect.getclosurevars(function).nonlocals
        if 'decorators' in closures:
            for func in closures['decorators']:
                if func.__name__ == func_name or func.__qualname__.split('.')[0] == func_name:
                    return True

        if 'method' in closures:
            return self._has_method_decorator(closures['method'], func_name)

        return False

    def _get_method_decorators(self, function):
        """
        Returns a generator of functions that decorate the provided function using
        ``@method_decorator``.
        """
        closures = inspect.getclosurevars(function).nonlocals
        if 'decorators' in closures:
            for func in closures['decorators']:
                yield func

        if 'method' in closures:
            yield from self._get_method_decorators(closures['method'])

    def _has_test_func(self, function):
        """
        Checks if the provided function is decorated with the ``user_passes_test`` decorator.
        """
        closures = inspect.getclosurevars(function).nonlocals
        if 'test_func' in closures:
            return True

        if 'view_func' in closures:
            return self._has_test_func(closures['view_func'])

        return False

    def _has_test_func_lambda(self, function, name):
        """
        Checks if the provided function's test_func contains the lambda expression ``name`` (str).
        """
        closures = inspect.getclosurevars(function).nonlocals
        if 'test_func' in closures:
            if name in inspect.getclosurevars(closures['test_func']).unbound:
                return True

        if 'decorators' in closures:
            for func in closures['decorators']:
                if self._has_test_func_lambda(func, name):
                    return True

        if 'method' in closures:
            return self._has_test_func_lambda(closures['method'], name)

        return False

    def _get_test_func_closures(self, function):
        closures = inspect.getclosurevars(function).nonlocals
        if 'test_func' in closures:
            yield inspect.getclosurevars(closures['test_func'])

        if 'view_func' in closures:
            yield from self._get_test_func_closures(closures['view_func'])

    def _has_func_decorator(self, function, func_name):
        closures = inspect.getclosurevars(function).nonlocals
        if 'test_func' in closures:
            test_closures = inspect.getclosurevars(closures['test_func']).unbound
            if func_name in test_closures:
                return True

            if 'view_func' in closures:
                return self._has_func_decorator(closures['view_func'], func_name)

        return False


class BaseFileredMixinProcessor(BaseCBVProcessor):
    """
    Base class for parsing mixins on class based views.
    Set ``class_filter`` to filter the class names the processor applies to.
    ONLY checks top level base classes.

    :var class_filter: initial value: ``None``
    """
    class_filter = None

    def can_process(self, view):
        if not super().can_process(view):
            return False

        view_bases = [cls.__module__ + '.' + cls.__name__ for cls in view.__bases__]

        for cls_filter in self.get_class_filter():
            if cls_filter in view_bases:
                return True

        return False

    def get_class_filter(self):
        """
        Override this method to override the class_names attribute.
        Must return an iterable.

        :return: a list of strings containing the full paths of mixins to detect.
        :raises ImproperlyConfigured: if the ``class_filter`` atribute is ``None``.
        """
        if self.class_filter is None:
            raise ImproperlyConfigured(
                '{0} is missing the class_filter attribute. Define {0}.class_filter, or override '
                '{0}.get_class_filter().'.format(self.__class__.__name__)
            )
        if isinstance(self.class_filter, str):
            cls_filter = (self.class_filter, )
        else:
            cls_filter = self.class_filter
        return cls_filter
