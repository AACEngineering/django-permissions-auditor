Changelog
=========

v0.5.1 (Released 9/23/2019)
------------------

- Add error message when multiple permissions are found for a single permission string in the django admin.


v0.5.0 (Released 2/12/2019)
------------------

- Override the django groups admin list instead of creating a custom one (this can be configured via ``PERMISSIONS_AUDITOR_ADMIN_OVERRIDE_GROUPS`` setting.)
- Add ``check_view_permissions`` management command.


v0.4.3 (Released 1/28/2019)
---------------------------

- Prevent the app from creating migrations


v0.4.2 (Released 1/23/2019)
---------------------------

- Fix permission check for groups listing (uses the default Django 'auth.change_group', 'auth.view_group')
- Fix N+1 query in groups listing


v0.4.1 (Released 1/22/2019)
---------------------------

- Hotfix for auth migrations issue


v0.4.0 (Release Removed)
---------------------------

- Add groups listing to admin site


v0.3.3 (Released 1/9/2019)
--------------------------

- Mark docstrings as safe in admin templates
- No longer suppress inner exceptions when parsing processors
- Fix Django admin module permissions check


v0.3.2 (Released 1/9/2019)
--------------------------

- Fix various cache issues
- Only show active users in the admin permission configuration page


v0.3.1 (Released 1/8/2019)
--------------------------

Initial stable release
