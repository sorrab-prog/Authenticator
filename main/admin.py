from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ['start_date', 'token_code']
    list_display = ('email', 'name', 'age', 'phone', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)