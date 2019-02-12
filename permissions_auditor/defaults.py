from django.conf import settings

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
PERMISSIONS_AUDITOR_BLACKLIST = {
    'namespaces': [
        'admin',
    ],
    'view_names': [],
    'modules': [],
}
PERMISSIONS_AUDITOR_ADMIN = True
PERMISSIONS_AUDITOR_ADMIN_OVERRIDE_GROUPS = True

PERMISSIONS_AUDITOR_ROOT_URLCONF = settings.ROOT_URLCONF

PERMISSIONS_AUDITOR_CACHE_KEY = 'permissions_auditor_views'
PERMISSIONS_AUDITOR_CACHE_TIMEOUT = 900
