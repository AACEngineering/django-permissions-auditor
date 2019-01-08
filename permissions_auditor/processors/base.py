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
        Get the permissions required on the provided view.
        Must return an iterable.

        :param view: the view being processed.
        :type view: function or class
        :return: the permissions required to access the view. Default: ``[]``
        :rtype: list(str)
        """
        return []

    def get_login_required(self, view):
        """
        Get whether or not the view needs the user to be logged in to access.

        :param view: the view being processed.
        :type view: function or class
        :return: whether a user must be logged in to access this view.
                 Default: ``False``
        :rtype: boolean or None (if unknown)
        """
        return False

    def get_docstring(self, view):
        """
        Return any additional information that should be displayed when
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


class BaseFileredMixinProcessor(BaseCBVProcessor):
    """
    Base class for parsing mixins on class based views.
    Set `class_filter` to filter the class names the processor applies to.
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
