from django import forms
from django.contrib.admin import widgets
from django.contrib.auth import get_user_model
from django.contrib.auth.models import ContentType, Group, Permission

User = get_user_model()


class AuditorAdminPermissionForm(forms.ModelForm):
    name = forms.CharField(disabled=True)
    content_type = forms.ModelChoiceField(ContentType.objects.all(), disabled=True)
    codename = forms.CharField(disabled=True)
    users = forms.ModelMultipleChoiceField(
        widget=widgets.FilteredSelectMultiple("User", is_stacked=False),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )
    groups = forms.ModelMultipleChoiceField(
        widget=widgets.FilteredSelectMultiple("Group", is_stacked=False),
        queryset=Group.objects.all(),
        required=False,
    )

    class Meta:
        model = Permission
        fields = (
            'name', 'content_type', 'codename',
            'users', 'groups',
        )
