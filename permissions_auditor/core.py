from collections import namedtuple

from django.conf import ImproperlyConfigured, settings
from django.contrib.admindocs.views import simplify_regex
from django.core.cache import cache
from django.urls.resolvers import RegexPattern, RoutePattern, URLPattern, URLResolver
from django.utils.module_loading import import_string

from . import defaults


def _get_setting(name):
    return getattr(settings, name, getattr(defaults, name))


def _get_blacklist(name):
    blacklist = _get_setting('PERMISSIONS_AUDITOR_BLACKLIST')

    # Fall back to the defauls if the user does not provide the specific
    # blacklist in their settings.
    if name not in blacklist:
        blacklist = getattr(defaults, 'PERMISSIONS_AUDITOR_BLACKLIST')

    return blacklist[name]


def _get_cache_key(base_url):
    prefix = _get_setting('PERMISSIONS_AUDITOR_CACHE_KEY')
    return '{}.{}'.format(prefix, base_url)


NAMESPACE_BLACKLIST = tuple(_get_blacklist('namespaces'))
VIEW_BLACKLIST = tuple(_get_blacklist('view_names'))
MODULE_BLACKLIST = tuple(_get_blacklist('modules'))

ViewDetails = namedtuple('ViewDetails', [
    'module', 'name', 'url', 'permissions', 'login_required', 'docstring'
])


class ViewParser:

    def __init__(self):
        self.load_processors()

    def load_processors(self):
        self._processors = []

        for processor_path in _get_setting('PERMISSIONS_AUDITOR_PROCESSORS'):

            try:
                processor = import_string(processor_path)
                self._processors.append(processor())
            except (ImportError, TypeError):
                raise ImproperlyConfigured(
                    '{} is not a valid permissions processor.'.format(processor_path)
                )

    def parse(self, view):
        """
        Process a view.

        Returns a tuple containing:
        permissions (list), login_required (boolean or None), docstring (str)
        """
        permissions = []
        login_required = False
        docstrings = []

        for processor in self._processors:
            if processor.can_process(view):
                permissions.extend(processor.get_permission_required(view))

                login_required_result = processor.get_login_required(view)
                if login_required_result is None and not login_required:
                    login_required = login_required_result
                else:
                    login_required = login_required_result or login_required

                docstrings.append(processor.get_docstring(view))

        return permissions, login_required, '\n'.join(list(set(filter(None, docstrings))))


def get_all_views(urlpatterns=None, base_url=''):
    """
    Get all views in the specified urlpatterns.

    If urlpatterns is not specified, uses the `PERMISSIONS_AUDITOR_ROOT_URLCONF`
    setting, which by default is the value of `ROOT_URLCONF` in your project settings.

    Returns a list of `View` namedtuples.
    """
    cache_key = _get_cache_key(base_url)
    cache_timeout = _get_setting('PERMISSIONS_AUDITOR_CACHE_TIMEOUT')

    views = cache.get(cache_key)

    if views is None:
        views = []

        if urlpatterns is None:
            root_urlconf = __import__(_get_setting('PERMISSIONS_AUDITOR_ROOT_URLCONF'))
            urlpatterns = root_urlconf.urls.urlpatterns

        parser = ViewParser()

        for pattern in urlpatterns:
            if isinstance(pattern, RoutePattern) or isinstance(pattern, URLResolver):

                if pattern.namespace in NAMESPACE_BLACKLIST:
                    continue

                # Recursively fetch patterns
                views.extend(get_all_views(pattern.url_patterns, base_url + str(pattern.pattern)))

            elif isinstance(pattern, URLPattern) or isinstance(pattern, RegexPattern):
                view = pattern.callback

                # If this is a CBV, use the actual class instead of the as_view() classmethod.
                view = getattr(view, 'view_class', view)

                full_view_path = '{}.{}'.format(view.__module__, view.__name__)
                if full_view_path in VIEW_BLACKLIST or view.__module__ in MODULE_BLACKLIST:
                    continue

                permissions, login_required, docstring = parser.parse(view)

                views.append(ViewDetails._make([
                    view.__module__,
                    view.__name__,
                    simplify_regex(base_url + str(pattern.pattern)),
                    permissions,
                    login_required,
                    docstring
                ]))

        cache.set(cache_key, views, cache_timeout)

    return views
