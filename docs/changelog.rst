Changelog
=========

v0.6.0 (Release TBD)
--------------------

- Refactored decorator processors.

    Added support for nested decorators:

    .. code-block:: python

        @staff_member_required
        @permission_required('auth.view_user')
        def my_view(request):
            ...

    Added support for decorators within ``@method_decorator`` on class based views:

    .. code-block:: python

        class MyView(View):
            @method_decorator(staff_member_required)
            @method_decorator(permission_required('auth.view_user'))
            def dispatch(self, request, *args, **kwargs):
                ...


v0.5.1 (Released 9/23/2019)
---------------------------

- Added error message when multiple permissions are found for a single permission string in the django admin.


v0.5.0 (Released 2/12/2019)
---------------------------

- The django Groups admin list is now overridden instead of adding a custom one (this can be configured via ``PERMISSIONS_AUDITOR_ADMIN_OVERRIDE_GROUPS`` setting.)
- Added ``check_view_permissions`` management command.


v0.4.3 (Released 1/28/2019)
---------------------------

- Prevented the app from creating migrations


v0.4.2 (Released 1/23/2019)
---------------------------

- Fixed permission check for groups listing (uses the default Django 'auth.change_group', 'auth.view_group')
- Fixed N+1 query in groups listing


v0.4.1 (Released 1/22/2019)
---------------------------

- Hotfix for auth migrations issue


v0.4.0 (Release Removed)
---------------------------

- Added groups listing to admin site


v0.3.3 (Released 1/9/2019)
--------------------------

- Marked docstrings as safe in admin templates
- No longer suppress inner exceptions when parsing processors
- Fixed Django admin module permissions check


v0.3.2 (Released 1/9/2019)
--------------------------

- Fixed various cache issues
- Only show active users in the admin permission configuration page


v0.3.1 (Released 1/8/2019)
--------------------------

- Initial stable release
