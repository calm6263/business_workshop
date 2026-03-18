# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Company

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профиль"
    fields = ('user_type', 'company', 'phone')
    extra = 0
    max_num = 1

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type', 'is_staff')
    list_filter = ('profile__user_type', 'is_staff', 'is_superuser', 'is_active')

    def get_inline_instances(self, request, obj=None):
        # Only show inline when editing an existing user (obj is not None)
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    def get_user_type(self, obj):
        return obj.profile.get_user_type_display() if hasattr(obj, 'profile') else '-'
    get_user_type.short_description = 'Тип пользователя'
    get_user_type.admin_order_field = 'profile__user_type'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'phone', 'created_at')
    search_fields = ('name', 'registration_number')