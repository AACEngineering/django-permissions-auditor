"Permissions auditing for Django."

__version__ = '1.0.5'

# This can be removed once Django 3.1 and below support is dropped.
from django import VERSION as DJANGO_VERSION
if DJANGO_VERSION < (3, 1):
    default_app_config = 'permissions_auditor.apps.PermissionsAuditorConfig'
