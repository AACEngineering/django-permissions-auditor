Management Commands
===================

check_view_permissions
----------------------

:synopsis: Checks that all detected view permissions exist in the database.

Uses permissions found on your project's views and compares the with the permissions
that exist within the database. Useful for catching typos when specifying permissions.


Example Usage
^^^^^^^^^^^^^

::

  $ python manage.py check_view_permissions



dump_view_permissions
----------------------

:synopsis: Dumps all detected view permissions to the specified output format.

If no parameters are provided, outputs JSON formatted results to ``stdout``.

Supports ``csv`` and ``json`` formats using ``--format`` or ``-f`` parameter.
Output to a file using ``--output`` or ``-o``, similar to Django's ``dumpdata`` command.

Example Usage
^^^^^^^^^^^^^

::

  $ python manage.py dump_view_permissions

  $ python manage.py dump_view_permissions --format csv

  $ python manage.py dump_view_permissions --format csv --output example_file.csv

  $ python manage.py dump_view_permissions --format json

  $ python manage.py dump_view_permissions --format csv --output example_file.json
