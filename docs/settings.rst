Settings
==================


.. _PERMISSIONS_AUDITOR_PROCESSORS:

PERMISSIONS_AUDITOR_PROCESSORS
--------------------------------------

This setting is used to configure the processors used to parse views for their permissions.
You can add custom processors, or remove the default ones similar to Django's middleware system.

For details on each processor, see :ref:`processors`.

Default::

    PERMISSIONS_AUDITOR_PROCESSORS = [
        'permissions_auditor.processors.auth_mixins.PermissionRequiredMixinProcessor',
        'permissions_auditor.processors.auth_mixins.LoginRequiredMixinProcessor',
        'permissions_auditor.processors.auth_mixins.UserPassesTestMixinProcessor',
        'permissions_auditor.processors.auth_decorators.PermissionRequiredDecoratorProcessor',
        'permissions_auditor.processors.auth_decorators.LoginRequiredDecoratorProcessor',
        'permissions_auditor.processors.auth_decorators.StaffMemberRequiredDecoratorProcessor',
        'permissions_auditor.processors.auth_decorators.SuperUserRequiredDecoratorProcessor',
        'permissions_auditor.processors.auth_decorators.UserPassesTestDecoratorProcessor',
    ]



.. _PERMISSIONS_AUDITOR_BLACKLIST:

PERMISSIONS_AUDITOR_BLACKLIST
--------------------------------------

Exclude views from parsing that match the blacklist values.

Default::

    PERMISSIONS_AUDITOR_BLACKLIST = {
        'namespaces': [
            'admin',
        ],
        'view_names': [],
        'modules': [],
    }

:namespaces: URL namespaces that will be blacklisted. By default, all views in the ``admin`` namespace are blacklisted.
:view_names: Fully qualified view paths to be blacklisted. Example: ``test_app.views.home_page``.
:modules: Modules to be blacklisted. Example: ``test_app.views.function_based``.



.. _PERMISSIONS_AUDITOR_ADMIN:

PERMISSIONS_AUDITOR_ADMIN
--------------------------------------

Enable or disable the Django admin page provided by the app. If ``TRUE``, the admin site will be enabled.
Useful if you want to create a custom management page instead of using the Django admin.

Default: ``TRUE``



.. _PERMISSIONS_AUDITOR_ADMIN_OVERRIDE_GROUPS:

PERMISSIONS_AUDITOR_ADMIN_OVERRIDE_GROUPS
-----------------------------------------

Override the default django groups admin with the permissions auditor version. Has no effect if
:ref:`PERMISSIONS_AUDITOR_ADMIN` is set to ``False``.

Default: ``True``



.. _PERMISSIONS_AUDITOR_ROOT_URLCONF:

PERMISSIONS_AUDITOR_ROOT_URLCONF
--------------------------------------

The root Django URL configuration to use when fetching views.

Default: The ``ROOT_URLCONF`` value in your Django project's ``settings.py`` file.



.. _PERMISSIONS_AUDITOR_CACHE_KEY:

PERMISSIONS_AUDITOR_CACHE_KEY
--------------------------------------

The cache key prefix to use when caching processed views results.

Default: ``'permissions_auditor_views'``



.. _PERMISSIONS_AUDITOR_CACHE_TIMEOUT:

PERMISSIONS_AUDITOR_CACHE_TIMEOUT
--------------------------------------

The timeout to use when caching processed views results.

Default: ``900``

