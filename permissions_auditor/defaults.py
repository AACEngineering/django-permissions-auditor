PERMISSIONS_PROCESSORS = [
    'permissions_config.processors.auth_mixins.PermissionRequiredMixinProcessor',
    'permissions_config.processors.auth_mixins.LoginRequiredMixinProcessor',
    'permissions_config.processors.auth_mixins.UserPassesTestMixinProcessor'
    'permissions_config.processors.auth_decorators.PermissionRequiredDecoratorProcessor',
    'permissions_config.processors.auth_decorators.LoginRequiredDecoratorProcessor',
    'permissions_config.processors.auth_decorators.StaffMemberRequiredDecoratorProcessor',
    'permissions_config.processors.auth_decorators.SuperUserRequiredDecoratorProcessor',
    'permissions_config.processors.auth_decorators.UserPassesTestDecoratorProcessor',
]
PERMISSIONS_BLACKLIST = {
    'namespaces': [],
    'views': []
}
