PERMISSIONS_PROCESSORS = [
    'permissions_auditor.processors.auth_mixins.PermissionRequiredMixinProcessor',
    'permissions_auditor.processors.auth_mixins.LoginRequiredMixinProcessor',
    'permissions_auditor.processors.auth_mixins.UserPassesTestMixinProcessor',
    'permissions_auditor.processors.auth_decorators.PermissionRequiredDecoratorProcessor',
    'permissions_auditor.processors.auth_decorators.LoginRequiredDecoratorProcessor',
    'permissions_auditor.processors.auth_decorators.StaffMemberRequiredDecoratorProcessor',
    'permissions_auditor.processors.auth_decorators.SuperUserRequiredDecoratorProcessor',
    'permissions_auditor.processors.auth_decorators.UserPassesTestDecoratorProcessor',
]
PERMISSIONS_BLACKLIST = {
    'namespaces': [],
    'views': []
}
