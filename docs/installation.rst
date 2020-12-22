Installation
============

Requirements:

* Django 2.2, 3.0, 3.1
* Python 3.6, 3.7, 3.8, 3.9


To install::

    pip install django-permissions-auditor


Add `permissions_auditor` to your ``INSTALLED_APPS`` in your project's ``settings.py`` file::

    INSTALLED_APPS = [
        ...
        'permissions_auditor',
        ...
    ]


That's it! A permissions auditor section will now show in your site's admin page. To fine tune what is displayed, head over to the :ref:`Settings` page.
