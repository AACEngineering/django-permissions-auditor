import inspect

from django.conf import ImproperlyConfigured


class BaseProcessor:

    def can_process(self, view):
        """
        Can this processor process the provided view?
        Useful when implementing filtering.
        """
        return True

    def get_permission_required(self, view):
        """
        Return the permissions required on the provided view.
        Must return an iterable.
        """
        return []

    def get_login_required(self, view):
        """
        Return True if the provided view requires the user to be loged in.
        """
        return False

    def get_docstring(self, view):
        """
        Return any additional information that should be displayed when
        showing permisison information.
        """
        return None


class BaseFuncViewProcessor(BaseProcessor):
    """Base class for function based views."""

    def can_process(self, view):
        return inspect.isfunction(view)


class BaseMixinProcessor(BaseProcessor):
    """Base class for parsing mixins on class based views."""

    def can_process(self, view):
        return inspect.isclass(view)


class BaseFileredMixinProcessor(BaseMixinProcessor):
    """
    Base class for parsing mixins on class based views.
    Override `class_filter` to filter the class names the processor applies to.
    ONLY checks top level base classes.
    """
    class_filter = None

    def can_process(self, view):
        if not super().can_process(view):
            return False

        view_bases = [cls.__module__ + '.' + cls.__name__ for cls in view.__bases__]

        for cls_filter in self.get_class_filter(view):
            if cls_filter in view_bases:
                return True

        return False

    def get_class_filter(self, view):
        """
        Override this method to override the class_names attribute.
        Must return an iterable.
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
