Example Views
=============

The following are example views are detected out of the box. For more examples, see
``permissions_auditor/tests/fixtures/views.py``.


Simple Permission Required Page
-------------------------------

.. code-block:: python
    :caption: views.py

    from django.contrib.auth.mixins import PermissionRequiredMixin
    from django.views.generic import TemplateView

    class ExampleView(PermissionRequiredMixin, TemplateView):
        template_name = 'example.html'
        permission_required = 'auth.view_user'

        ...


.. code-block:: python
    :caption: urls.py

    from django.urls import path
    from views import ExampleView

    urlpatterns = [
        path('', ExampleView.as_view(), name='example'),
    ]


Result:

+-------------+-----+---------------------+----------------+------------------+
| Name        | URL | Permission Required | Login Required | Additional Info  |
+=============+=====+=====================+================+==================+
| ExampleView | `/` | ``auth.view_user``  | True           |                  |
+-------------+-----+---------------------+----------------+------------------+



Custom Permission Required Page
--------------------------------

In this example, we only want users with the first name 'bob' to be able to
access the page.

.. code-block:: python
    :caption: views.py

    from django.contrib.auth.mixins import PermissionRequiredMixin
    from django.views.generic import TemplateView

    class BobView(PermissionRequiredMixin, TemplateView):
        template_name = 'example.html'

        def has_permission(self):
            """
            Only users with the first name Bob can access.
            """
            return self.request.user.first_name == 'Bob'

        ...


.. code-block:: python
    :caption: urls.py

    from django.urls import path
    from views import BobView

    urlpatterns = [
        path('/bob/', BobView.as_view(), name='bob'),
    ]


Result:

+-------------+---------+---------------------+----------------+----------------------------+
| Name        | URL     | Permission Required | Login Required | Additional Info            |
+=============+=========+=====================+================+============================+
| ExampleView | `/bob/` |                     | True           | Only users with the first  |
|             |         |                     |                | name Bob can access.       |
+-------------+---------+---------------------+----------------+----------------------------+

.. hint::
    The :ref:`PermissionRequiredMixinProcessor` will display the docstring on the the
    ``has_permission()`` function in the additional info column.



Simple Login Required View
--------------------------

.. code-block:: python
    :caption: views.py

    from django.contrib.auth.decorators import login_required

    @login_required
    def my_view(request):
        ...


.. code-block:: python
    :caption: urls.py

    from django.urls import path
    from views import my_view

    urlpatterns = [
        path('', my_view, name='example'),
    ]


Result:

+-------------+-----+---------------------+----------------+------------------+
| Name        | URL | Permission Required | Login Required | Additional Info  |
+=============+=====+=====================+================+==================+
| my_view     | `/` |                     | True           |                  |
+-------------+-----+---------------------+----------------+------------------+
