from django.contrib import admin
from django.db import models
from django.template.response import TemplateResponse
from django.urls import path, reverse


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
            path('by_app/', self.admin_site.admin_view(self.permissions_by_app)),
        ]
        return auditor_urls

    def permissions_index(self, request):
        context = dict(self.admin_site.each_context(request))
        return TemplateResponse(
            request, "permissions_auditor/admin/index.html", context
        )

    def permissions_by_app(self, request):
        context = dict(self.admin_site.each_context(request))
        return TemplateResponse(
            request, "permissions_auditor/admin/permissions_by_app.html", context
        )
