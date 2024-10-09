from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile

# Custom UserAdmin for managing CustomUser in admin interface
class UserAdmin(BaseUserAdmin):
    # Fields to be used in displaying the User model.
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()

# Register UserProfile with the admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'date_of_birth')
    search_fields = ('user__email', 'phone_number')

# Register CustomUser and UserProfile with the Django admin
admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
