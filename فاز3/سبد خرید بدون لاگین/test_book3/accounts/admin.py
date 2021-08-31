from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Address, Membership
from django.contrib.auth.models import Group


class UserAddressInline(admin.StackedInline):
    model = Address
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserAddressInline]
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('full_name', 'email', 'is_admin', 'is_staffs', 'created')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Main', {'fields': ('full_name', 'email', 'password')}),
        ('Personal info', {'fields': ('is_active',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staffs',)})
    )
    add_fieldsets = (
        (None, {
            'fields': ('full_name', 'email', 'password1', 'password2',)
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    list_editable = ['email', 'is_admin', 'is_staffs']
    filter_horizontal = ()


@admin.register(Address)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'town_city', 'address_line', 'default']
    list_filter = ['town_city', 'full_name']
    list_editable = ['town_city', 'default', 'address_line']
    search_fields = ['full_name']


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


admin.site.register(Group, GroupAdmin)
