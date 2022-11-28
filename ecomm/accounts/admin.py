from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','last_name')
admin.site.register(CustomUserModel,CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','mobile_number','city','country')
admin.site.register(UserProfile,UserProfileAdmin)


admin.site.register(ContactUs)