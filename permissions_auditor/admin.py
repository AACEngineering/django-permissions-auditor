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
            path('', self.admin_site.admin_view(self.permissions_index),
                 name='%s_%s_changelist' % info),
            path('by_module/', self.admin_site.admin_view(self.views_by_module)),
        ]
        return auditor_urls

    def permissions_index(self, request):
        context = dict(self.admin_site.each_context(request))
        return TemplateResponse(
            request, "permissions_auditor/admin/index.html", context
        )

    def views_by_module(self, request):
        context = dict(self.admin_site.each_context(request))

        root_urlconf = __import__(settings.ROOT_URLCONF)
        all_urlpatterns = root_urlconf.urls.urlpatterns
        views = get_views_by_module(all_urlpatterns)

        grouped_views = {}
        for key, views_list in groupby(views, lambda x: x[0]):
            for view in views_list:
                grouped_views.setdefault(key, []).append(view[1:])

        context.update({
            'views': grouped_views
        })
        return TemplateResponse(
            request, "permissions_auditor/admin/views_by_module.html", context
        )
