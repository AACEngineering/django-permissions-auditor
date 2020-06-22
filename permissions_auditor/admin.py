from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from permissions_auditor.core import get_views, _get_setting
from permissions_auditor.forms import AuditorAdminPermissionForm


class View(models.Model):
    """Dummy model to display views index pages in the admin."""
    class Meta:
        managed = False
        verbose_name = 'permission'
        verbose_name_plural = _('Site Views')
        app_label = 'permissions_auditor'


class ViewsIndexAdmin(admin.ModelAdmin):
    """
    Index containing all of the views found on the django site,
    and the permissions needed to access them.
    """
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
        try:
            app_label, codename = permission.split('.')
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
        try:
            obj = self.get_object(request, permission)
        except Permission.MultipleObjectsReturned:
            return self._get_obj_multiple_exist_redirect(request, permission)

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
        return self.has_view_permission(request)

    def has_auditor_change_permission(self, request):
        return request.user.has_perms(['auth.change_user', 'auth.change_group'])

    def _get_obj_multiple_exist_redirect(self, request, permission):
        """
        Create a message informing the user that multiple permissions were found
        for the specified permission string, and return to the admin index page.
        """
        msg = _('Found multiple permissions when looking up “%(permission)s”. '
                'Please ensure only a single permission exists with this name.') % {
            'permission': permission
        }
        self.message_user(request, msg, messages.WARNING)
        url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(url)


class AuditorGroupAdmin(GroupAdmin):
    list_display = ['name', 'permissions_display', 'users_display']

    def permissions_display(self, obj):
        result = ''
        for perm in obj.permissions.all():
            perm_str = '{}.{}'.format(perm.content_type.app_label, perm.codename)
            url = reverse('admin:permissions_auditor_view_permissiondetail', args=(perm_str,))
            result += '<a href="{}">{}</a><br/>'.format(url, perm_str)
        return mark_safe(result)

    permissions_display.short_description = 'Permissions'

    def users_display(self, obj):
        result = ''
        for user in obj.active_users:
            url = reverse('admin:auth_user_change', args=(user.pk,))
            result += '<a href="{}">{}</a><br/>'.format(url, user)
        return mark_safe(result)

    users_display.short_description = 'Active Users'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(
            'permissions',
            'permissions__content_type',
            Prefetch(
                'user_set',
                queryset=get_user_model().objects.filter(is_active=True),
                to_attr='active_users'
            )
        )


if _get_setting('PERMISSIONS_AUDITOR_ADMIN'):
    admin.site.register(View, ViewsIndexAdmin)

    if _get_setting('PERMISSIONS_AUDITOR_ADMIN_OVERRIDE_GROUPS'):
        admin.site.unregister(Group)
        admin.site.register(Group, AuditorGroupAdmin)
