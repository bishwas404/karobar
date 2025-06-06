from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _
from .models import Party, Transaction

class UserAdmin(BaseUserAdmin):
  ordering=['id']
  list_display=['email','name']
  fieldsets=(
    (None,{'fields':('email','password',)}),
    (_('permissions'),{'fields':('is_active','is_staff','is_superuser',)}),
    (_('Important dates'),{'fields':('last_login',)}),

  )
  readonly_field=['lastlogin']

  add_fieldsets=(
    (None,{'classes':('wide',),'fields':(
      'email',
      'password1',
      'password2',
      'name',
      'is_active',
      'is_staff',
      'is_superuser',
    )}),
  )
admin.site.register(models.User,UserAdmin)
admin.site.register(Party)
admin.site.register(Transaction)