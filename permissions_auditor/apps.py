from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PermissionsAuditorConfig(AppConfig):
    name = 'permissions_auditor'
    verbose_name = _('Permissions Auditor')
