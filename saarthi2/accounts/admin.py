from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone', 'user', 'otp_verified', 'created_at')
    list_filter = ('otp_verified', 'created_at')
    search_fields = ('phone', 'user__username')
