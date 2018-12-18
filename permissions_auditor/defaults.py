PERMISSIONS_PROCESSORS = [
    # Class Based
    'permissions_config.processors.PermissionRequiredMixinProcessor',
    'permissions_config.processors.LoginRequiredMixinProcessor',
    'permissions_config.processors.UserPassesTestMixinProcessor'
    # Function Based
    'permissions_config.processors.PermissionRequiredDecoratorProcessor',
    'permissions_config.processors.LoginRequiredDecoratorProcessor'
]
PERMISSIONS_NAMESPACE_FILTER = []
PERMISSIONS_VIEW_NAME_FILTER = []
