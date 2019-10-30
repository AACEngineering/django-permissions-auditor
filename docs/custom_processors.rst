Custom Processors
===========================

Base Processors
---------------

All processors inherit from ``BaseProcessor``.

.. autoclass:: permissions_auditor.processors.base.BaseProcessor
    :members:


Other useful base classes:

.. autoclass:: permissions_auditor.processors.base.BaseFuncViewProcessor

.. autoclass:: permissions_auditor.processors.base.BaseCBVProcessor

.. autoclass:: permissions_auditor.processors.base.BaseDecoratorProcessor

.. autoclass:: permissions_auditor.processors.base.BaseFileredMixinProcessor
    :members: class_filter, get_class_filter


Parsing Mixins
--------------

Creating a custom processor for mixins on class based views is fairly straight forward.

In this example, we have a mixin ``BobRequiredMixin`` and a view that uses it, ``BobsPage``.
The mixin should only allow users with the first name Bob to access the page.


.. code-block:: python
    :caption: example_project/views.py

    from django.core.exceptions import PermissionDenied
    from django.views.generic import TemplateView

    class BobRequiredMixin:
        def dispatch(self, request, *args, **kwargs):
            if self.request.user.first_name != 'Bob':
                raise PermissionDenied("You are not Bob")
            return super().dispatch(request, *args, **kwargs)

    class BobsPage(BobRequiredMixin, TemplateView):
        ...


Let's define our processor in `processors.py`.

.. code-block:: python
    :caption: example_project/processors.py

    from permissions_auditor.processors.base import BaseFileredMixinProcessor

    class BobRequiredMixinProcessor(BaseFileredMixinProcessor):
        class_filter = 'example_project.views.BobRequiredMixin'

        def get_login_required(self, view):
            return True

        def get_docstring(self, view):
            return "The user's first name must be Bob to view."


To register our processor, we need to add it to :ref:`PERMISSIONS_AUDITOR_PROCESSORS`
in our project settings.


.. code-block:: python
    :caption: settings.py
    :emphasize-lines: 4

    PERMISSIONS_AUDITOR_PROCESSORS = [
        ...

        'example_project.processors.BobRequiredProcessor',
    ]


When ``BobsPage`` is registered to a URL, we should see this in the admin panel:

+-------------+-----+---------------------+----------------+--------------------------------------------+
| Name        | URL | Permission Required | Login Required | Additional Info                            |
+=============+=====+=====================+================+============================================+
| BobsPage    | `/` |                     | True           | The user's first name must be Bob to view. |
+-------------+-----+---------------------+----------------+--------------------------------------------+


Perhaps we want to make our mixin configurable so we can detect different names depending on the view.
We also have multiple people with the same first name, so we also want to check for a permission:
``example.view_pages``.


.. code-block:: python

    class FirstNameRequiredMixin:
        required_first_name = ''

        def dispatch(self, request, *args, **kwargs):
            if not (self.request.user.has_perm('example_app.view_userpages')
                    and self.request.user.first_name == self.required_first_name):
                raise PermissionDenied()
            return super().dispatch(request, *args, **kwargs)

    class GeorgesPage(FirstNameRequiredMixin, TemplateView):
        required_first_name = 'George'

        ...

We'll modify ``class_filter`` and ``get_docstring()`` from our old processor, and override
``get_permission_required()``.

.. code-block:: python

    from permissions_auditor.processors.base import BaseFileredMixinProcessor

    class FirstNameRequiredMixinProcessor(BaseFileredMixinProcessor):
        class_filter = 'example_project.views.FirstNameRequiredMixin'

        def get_permission_required(self, view):
            return ['example.view_pages']

        def get_login_required(self, view):
            return True

        def get_docstring(self, view):
            return "The user's first name must be {} to view.".format(view.first_name_required)


Once we register our view to a URL and register the processor, our admin table should look like this:

+-------------+-----+---------------------+----------------+-----------------------------------------------+
| Name        | URL | Permission Required | Login Required | Additional Info                               |
+=============+=====+=====================+================+===============================================+
| GeorgesPage | `/` | example.view_pages  | True           | The user's first name must be George to view. |
+-------------+-----+---------------------+----------------+-----------------------------------------------+


Additional Examples
-------------------

See the ``permissions_auditor/processors/`` folder in the source code for more examples.
