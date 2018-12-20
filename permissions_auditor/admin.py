from itertools import groupby

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.template.response import TemplateResponse
from django.urls import path

from permissions_auditor.core import get_views_by_module


class Index(models.Model):
    """Dummy model to display our pages in the admin."""
    class Meta:
        verbose_name_plural = 'Site Views Index'
        app_label = 'permissions_auditor'


@admin.register(Index)
class PermissionsAuditorAdmin(admin.ModelAdmin):

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name

        auditor_urls = [
            path('', self.admin_site.admin_view(self.views_by_module),
                 name='%s_%s_changelist' % info),
        ]
        return auditor_urls

    def views_by_module(self, request):
        context = dict(self.admin_site.each_context(request))

        root_urlconf = __import__(settings.ROOT_URLCONF)
        all_urlpatterns = root_urlconf.urls.urlpatterns

        context.update({
            'views': get_views_by_module(all_urlpatterns),
            'group_by': request.GET.get('group_by', 'module')
        })
        return TemplateResponse(
            request, "permissions_auditor/admin/views_list.html", context
        )
