PERMISSIONS_PROCESSORS = [
    'permissions_config.processors.mixins.PermissionRequiredMixinProcessor',
    'permissions_config.processors.mixins.LoginRequiredMixinProcessor',
    'permissions_config.processors.mixins.UserPassesTestMixinProcessor'
    'permissions_config.processors.decorators.PermissionRequiredDecoratorProcessor',
    'permissions_config.processors.decorators.LoginRequiredDecoratorProcessor',
    'permissions_config.processors.decorators.StaffMemberRequiredDecoratorProcessor',
    'permissions_config.processors.decorators.SuperUserRequiredDecoratorProcessor',
    'permissions_config.processors.decorators.UserPassesTestDecoratorProcessor',
]
PERMISSIONS_BLACKLIST = {
    'namespaces': [],
    'views': []
}
