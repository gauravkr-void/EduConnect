from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # This defines how the list of users looks in the admin dashboard
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    
    # This allows you to filter users by role or status
    list_filter = ('role', 'is_staff', 'is_active')
    
    # This tells Django which fields to show when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': (
            'full_name', 
            'role', 
            'contact_number', 
            'profile_picture',
            'terms_accepted',
            'is_email_verified'
        )}),
        ('Teacher Info', {'fields': ('institution_name', 'department', 'employee_id')}),
        ('Student Info', {'fields': ('roll_number', 'course_year', 'section_batch')}),
    )
    
    # This is for the "Add User" form in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'full_name', 'role')}),
    )

    ordering = ('email',)

# Register your model with the custom admin class
admin.site.register(User, CustomUserAdmin)