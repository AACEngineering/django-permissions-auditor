from django.contrib import admin
from django.db import models
from django.template.response import TemplateResponse
from django.urls import path

from permissions_auditor.core import get_all_views, _get_setting


if _get_setting('PERMISSIONS_AUDITOR_ADMIN'):

    class Index(models.Model):
        """Dummy model to display our pages in the admin."""
        class Meta:
            verbose_name_plural = 'Site Views Index'
            app_label = 'permissions_auditor'

    @admin.register(Index)
    class PermissionsAuditorAdmin(admin.ModelAdmin):

        def get_urls(self):
            info = self.model._meta.app_label, self.model._meta.model_name
            return [
                path('', self.admin_site.admin_view(self.index), name='%s_%s_changelist' % info),
            ]

        def index(self, request):
            context = dict(self.admin_site.each_context(request))

            context.update({
                'views': get_all_views(),
                'group_by': request.GET.get('group_by', 'module')
            })
            return TemplateResponse(
                request, "permissions_auditor/admin/views_index.html", context
            )

        def has_view_permission(self, request, obj=None):
            return request.user.is_staff

        def has_add_permission(self, request, obj=None):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False
