from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.urls.resolvers import RegexPattern, RoutePattern, URLPattern, URLResolver
from django.utils.module_loading import import_string

import defaults


def get_setting(name):
    return getattr(settings, name, getattr(defaults, name))


class ViewParser:

    def __init__(self):
        self.load_processors()

    def load_processors(self):
        self._processors = []

        for processor_path in get_setting('PERMISSIONS_PROCESSORS'):
            processor = import_string(processor_path)
            self._processors.append(processor())

    def parse(self, view):
        """
        Process a view.
        Returns the permissions required, if login is required, and any docstrings.
        """
        permissions = []
        login_required = False
        docstrings = []

        for processor in self._processors:
            if processor.can_process(view):
                permissions.extend(processor.get_permission_required(view))
                login_required = processor.get_login_required(view) or login_required
                docstrings.append(processor.get_docstring(view))

        return permissions, login_required, '\n'.join(list(set(filter(None, docstrings))))


def get_views(urlpatterns, base_url=''):
    """
    Get all views in the specified urlpatterns.
    """
    views = []

    parser = ViewParser()

    for pattern in urlpatterns:
        if isinstance(pattern, RoutePattern) or isinstance(pattern, URLResolver):

            # TODO: Namespace filtering
            # pattern.namespace

            # Recursively fetch patterns
            views.extend(get_views(pattern.url_patterns, base_url + str(pattern.pattern)))

        elif isinstance(pattern, URLPattern) or isinstance(pattern, RegexPattern):
            view = pattern.callback

            # If this is a CBV, use the actual class instead of the as_view() classmethod.
            view = getattr(view, 'view_class', view)

            # TODO: view name / module filtering
            # view.__module__ view.__name__

            permissions, login_required, docstring = parser.parse(view)

            views.append([
                view.__module__,
                view.__name__,
                simplify_regex(base_url + str(pattern.pattern)),
                permissions,
                login_required,
                docstring
            ])

    return views
