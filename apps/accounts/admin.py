# coding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


User = get_user_model()
from .models import Profile, Role, DepartmentKT, SubdepartmentKT, Log
from .forms import UserAdminChangeForm, UserAdminCreationForm


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'role', 'department', 'subdepartment', 'admin', 'staff', 'active', )
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_filter = ('username', 'role', 'department', 'subdepartment',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'department', 'subdepartment')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'department', 'subdepartment', 'password1', 'password2')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def get_user_role(self, obj):
        return obj.user.user_role
    get_user_role.short_description = 'Роль пользователя'
    get_user_role.admin_order_field = 'user__role'

    def get_role(self, obj):
        return obj.user.get_role_display()
    get_user_role.short_description = 'Роль'
    get_user_role.admin_order_field = 'user__role'

    def get_user_department(self, obj):
        return obj.user.user_department
    get_user_department.short_description = 'Отдел пользователя'
    get_user_department.admin_order_field = 'user__department'

    def get_department(self, obj):
        return obj.user.get_department_display()
    get_user_department.short_description = 'Отдел'
    get_user_department.admin_order_field = 'user__department'
#
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'position', 'online', )
    list_filter = ('last_name', 'online',)
    search_fields = ('first_name', 'last_name' )

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_at', 'end_time')

admin.site.register(User, CustomUserAdmin)
admin.site.register(DepartmentKT)
admin.site.register(SubdepartmentKT)
admin.site.register(Role)
