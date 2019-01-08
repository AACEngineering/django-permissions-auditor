from django.apps import AppConfig
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from permissions_auditor.core import _get_setting


class PermissionsAuditorConfig(AppConfig):
    name = 'permissions_auditor'
    verbose_name = _('Permissions Auditor')

    def ready(self):
        # Delete the cached views list on application reload.
        cache.delete_many([
            _get_setting('PERMISSIONS_AUDITOR_CACHE_KEY'),
            _get_setting('PERMISSIONS_AUDITOR_CACHE_KEY') + '_BASE_URL',
        ])
