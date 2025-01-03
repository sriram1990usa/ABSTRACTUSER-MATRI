from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Profile)

class AddimgAdmin(admin.ModelAdmin):
    model = Addimg 
    list_display = ['profile', 'propic', 'propic_hash']

admin.site.register(Addimg, AddimgAdmin)