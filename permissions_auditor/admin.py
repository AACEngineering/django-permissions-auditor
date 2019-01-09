from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.auth.models import Permission
from django.db import models
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from permissions_auditor.core import get_views, _get_setting
from permissions_auditor.forms import AuditorAdminPermissionForm


class Index(models.Model):
    """Dummy model to display our pages in the admin."""
    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = _('Site Views Index')
        app_label = 'permissions_auditor'


class ViewIndex(admin.ModelAdmin):
    form = AuditorAdminPermissionForm
    fieldsets = (
        (_('Permission Info'), {
            'fields': ('name', 'content_type', 'codename'),
        }),
        (_('Objects with this Permission'), {
            'fields': ('users', 'groups'),
        }),
    )

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return [
            path('', self.admin_site.admin_view(self.index), name='%s_%s_changelist' % info),
            path('<str:permission>/',
                 self.admin_site.admin_view(self.permission_detail),
                 name='%s_%s_permissiondetail' % info),
        ]

    def get_object(self, request, permission, from_field=None):
        app_label, codename = permission.split('.')
        try:
            return Permission.objects.get(content_type__app_label=app_label, codename=codename)
        except (Permission.DoesNotExist, ValueError):
            return None

    def get_form(self, request, obj, change=False, **kwargs):
        defaults = {
            'users': obj.user_set.filter(is_active=True),
            'groups': obj.group_set.all()
        }
        return self.form(request.POST or defaults, instance=obj)

    def index(self, request):
        context = dict(self.admin_site.each_context(request))

        context.update({
            'views': get_views(),
            'group_by': request.GET.get('group_by', 'module')
        })
        return TemplateResponse(request, "permissions_auditor/admin/views_index.html", context)

    def permission_detail(self, request, permission, obj=None):
        obj = self.get_object(request, permission)
        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, permission)

        opts = self.model._meta

        adminForm = helpers.AdminForm(
            self.get_form(request, obj),
            list(self.get_fieldsets(request, obj)),
            {},
            model_admin=self
        )
        media = self.media + adminForm.media

        if (request.method == 'POST' and
                adminForm.form.is_valid() and
                self.has_auditor_change_permission(request)):
            obj.user_set.set(adminForm.form.cleaned_data['users'])
            obj.group_set.set(adminForm.form.cleaned_data['groups'])
            return self.response_change(request, obj)

        context = {
            **self.admin_site.each_context(request),
            'adminform': adminForm,
            'errors': helpers.AdminErrorList(adminForm.form, []),
            'media': media,

            'views': get_views(),
            'permission': '{}.{}'.format(obj.content_type.app_label, obj.codename),

            'opts': opts,
            'add': False,
            'change': True,
            'is_popup': False,
            'save_as': self.save_as,
            'has_editable_inline_admin_formsets': False,
            'has_view_permission': self.has_view_permission(request, obj),
            'has_add_permission': self.has_add_permission(request, obj),
            'has_change_permission': self.has_auditor_change_permission(request),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'app_label': opts.app_label,
        }

        return TemplateResponse(
            request, "permissions_auditor/admin/permission_detail.html", context
        )

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_auditor_change_permission(self, request):
        return request.user.has_perms(['auth.change_user', 'auth.change_group'])


if _get_setting('PERMISSIONS_AUDITOR_ADMIN'):
    admin.site.register(Index, ViewIndex)
