Custom Processors
===========================

Intro
-----

All processors inherit from ``BaseProcessor``.

.. autoclass:: permissions_auditor.processors.base.BaseProcessor
    :members:


Other useful base classes:

.. autoclass:: permissions_auditor.processors.base.BaseFuncViewProcessor

.. autoclass:: permissions_auditor.processors.base.BaseCBVProcessor

.. autoclass:: permissions_auditor.processors.base.BaseFileredMixinProcessor
    :members: class_filter, get_class_filter


Class Based Views
-----------------

Creating a custom processor for class based views is fairly straight forward.

Here's an example of a mixin we want to detect:


.. code-block:: python
    :caption: example_project/views.py
    
    from django.contrib.auth.mixins import PermissionRequiredMixin
    from django.views.generic import TemplateView

    class BobRequiredMixin(PermissionRequiredMixin):
        def has_permission(self):
            return self.request.user.first_name == 'Bob'


    class BobsPage(BobRequiredMixin, TemplateView):
        ...


Our processor could look like this::

    from permissions_auditor.processors.base import BaseFileredMixinProcessor

    class BobRequiredMixinProcessor(BaseFileredMixinProcessor):
        class_filter = 'example_project.views.BobRequiredMixin'

        def get_docstring(self, view):
            return 'Your first name must be bob to view.'

