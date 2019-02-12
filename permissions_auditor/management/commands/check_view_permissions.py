from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from permissions_auditor.core import get_views


class Command(BaseCommand):
    help = 'Parse all view permissions, and find any that are missing from the database.'

    def get_view_permissions(self):
        views = get_views()
        permissions = []

        for view in views:
            permissions.extend(view.permissions)

        return list(set(permissions))

    def get_db_permissions(self):
        permissions = Permission.objects.all().values_list('content_type__app_label', 'codename')
        return ["{}.{}".format(ct, codename) for ct, codename in permissions]

    def handle(self, *args, **options):
        view_permissions = self.get_view_permissions()
        db_permissions = self.get_db_permissions()
        missing_perms = []

        for permission in view_permissions:
            if permission not in db_permissions:
                missing_perms.append(permission)

        if missing_perms:
            for permission in missing_perms:
                self.stdout.write(self.style.WARNING(
                    'Warning: No database entry found for permission `{}`.'.format(permission)
                ))
        else:
            self.stdout.write(self.style.SUCCESS('No permissions without database entries found.'))
