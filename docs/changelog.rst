Changelog
=========

v1.0.4 (Release TBD)
--------------------

- Changed AuditorGroupAdmin to use the User model's default manager.
- Confirmed support for Django 3.2.


v1.0.3 (Released 2/15/2021)
---------------------------

- Fixed invalid URL on AuditorGroupAdmin when using a custom user model (#11). Thanks @LerikG.
- Temporarily removed testing on django master.


v1.0.2 (Released 1/4/2021)
--------------------------

- Changed "No Grouping" filter to order by URL instead of view name.
- Added ``django.views.generic.base.RedirectView`` to the default ``view_names`` blacklist.
- Prevented duplicate permissions from being returned for a single view.
- Dropped testing support for python 3.5, which reached end of life in September 2020.


v1.0.1 (Released 7/1/2020)
--------------------------

- Fix admin error when looking up malformed permission strings.


v1.0.0 (Released 12/4/2019)
---------------------------

- Decorator processor improvements.

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

- Refactored test suite to be much cleaner.


v0.5.1 (Released 9/23/2019)
---------------------------

- Added error message when multiple permissions are found for a single permission string in the django admin.


v0.5.0 (Released 2/12/2019)
---------------------------

- The django Groups admin list is now overridden instead of adding a custom one (this can be configured via ``PERMISSIONS_AUDITOR_ADMIN_OVERRIDE_GROUPS`` setting.)
- Added ``check_view_permissions`` management command.


v0.4.3 (Released 1/28/2019)
---------------------------

- Fixed an issue which caused the app to create migrations for models that didn't exist.


v0.4.2 (Released 1/23/2019)
---------------------------

- Fixed permission check for groups listing (uses the default Django 'auth.change_group', 'auth.view_group')
- Fixed N+1 query in groups listing


v0.4.1 (Released 1/22/2019)
---------------------------

- Fixed app inadvertently creating migrations on the `Group` model.


v0.4.0 (Release Removed)
---------------------------

- Added groups listing to the admin site.


v0.3.3 (Released 1/9/2019)
--------------------------

- Marked docstrings as safe in admin templates.
- Inner exceptions on processors are no longer suppressed when parsing views.
- Fixed Django admin module permissions check.


v0.3.2 (Released 1/9/2019)
--------------------------

- Fixed various cache issues
- Only show active users in the admin permission configuration page


v0.3.1 (Released 1/8/2019)
--------------------------

- Initial stable release
