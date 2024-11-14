from django.contrib import admin
from .models import User, Job, Location, Salary, Image
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'age', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}), 
    )
    
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}), 
        ('Personal info', {'fields': ('name', 'age', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}), 
    )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

admin.site.register(Job)
admin.site.register(Location)
admin.site.register(Salary)
admin.site.register(Image)
