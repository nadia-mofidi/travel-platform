from django.contrib import admin
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.



class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_author',
        'is_staff',
        'is_active',
    )

    @admin.display(boolean=True, description='Authors')
    def is_author(self, obj):
        return obj.groups.filter(name='Authors').exists()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)