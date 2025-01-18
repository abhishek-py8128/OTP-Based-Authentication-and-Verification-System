from django.contrib import admin
from polls.models import User

# Register your models here.
class AdminUser(admin.ModelAdmin) :
    list_display = ['id', 'email', 'phone', 'is_email_verified', 'is_phone_verified', 'otp', 'email_verification_token']

admin.site.register(User, AdminUser)