from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# 将profile关联到user中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# 重新注册user
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
