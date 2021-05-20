"Permissions auditing for Django."

import django


__version__ = '1.0.4'


if django.VERSION < (3, 2):
    default_app_config = 'permissions_auditor.apps.PermissionsAuditorConfig'
