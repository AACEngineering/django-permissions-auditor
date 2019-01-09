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
            except (ImportError, TypeError) as ex:
                raise ImproperlyConfigured(
                    '{} is not a valid permissions processor.'.format(processor_path)
                ) from ex

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


def _get_views(urlpatterns=None, base_url=''):
    """
    Recursively fetch all views in the specified urlpatterns.

    If urlpatterns is not specified, uses the `PERMISSIONS_AUDITOR_ROOT_URLCONF`
    setting, which by default is the value of `ROOT_URLCONF` in your project settings.

    Returns a list of `View` namedtuples.
    """
    views = []

    if urlpatterns is None:
        root_urlconf = import_string(_get_setting('PERMISSIONS_AUDITOR_ROOT_URLCONF'))
        urlpatterns = root_urlconf.urlpatterns

    parser = ViewParser()

    for pattern in urlpatterns:
        if isinstance(pattern, RoutePattern) or isinstance(pattern, URLResolver):

            if pattern.namespace in NAMESPACE_BLACKLIST:
                continue

            # Recursively fetch patterns
            views.extend(_get_views(pattern.url_patterns, base_url + str(pattern.pattern)))

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

    return views


def get_views(urlpatterns=None, base_url=''):
    """
    Get a cached version of _get_views().
    """
    cache_key = _get_setting('PERMISSIONS_AUDITOR_CACHE_KEY')
    cache_base_url_key = cache_key + '_BASE_URL'
    cache_timeout = _get_setting('PERMISSIONS_AUDITOR_CACHE_TIMEOUT')

    cache_content = cache.get_many([cache_key, cache_base_url_key])
    views = cache_content.get(cache_key, None)
    cached_base_url = cache_content.get(cache_base_url_key, None)

    if views is None or cached_base_url != base_url:
        views = _get_views(urlpatterns, base_url)
        cache.set_many({
            cache_key: views,
            cache_base_url_key: base_url
        }, timeout=cache_timeout)

    return views
