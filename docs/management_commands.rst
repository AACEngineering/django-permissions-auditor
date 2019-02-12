Management Commands
===================

check_view_permissions
----------------------

:synopsis: Checks that all detected view permissions exist in the database.

Uses permissions found on your project's views and compares the with the permissions
that exist within the database. Useful for catching typos when specifying permissions.


Example Usage
-------------

::

  $ python manage.py check_view_permissions

