from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
from .forms import UserAdminCreationForm, UserAdminChangeForm
# User = get_user_model()

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PhoneOTP, User

admin.site.register(PhoneOTP)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('name', 'phone', 'admin', 'balance', 'clinic_find')
    list_filter = ('staff', 'active', 'admin',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': (('name', 'last_name', 'middle_name'), 'birth_date', 'age', 'balance',
                                      'clinic_find', 'email')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
         ),
    )

    search_fields = ('phone', 'name')
    ordering = ('phone', 'name')
    filter_horizontal = ()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
