from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User,Shops,UserData


class ProfileInline(admin.StackedInline):
    model = Shops
    max_num = 1
    can_delete = False
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('last_name','first_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


    list_display = ('last_name', 'first_name', 'email', 'is_staff')

    search_fields = ('email', 'first_name', 'last_name')

    ordering = ('email',)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(UserData)