from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
from advisorapp import models
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'admin', 'active')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('active', 'admin','staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(models.Advisor)