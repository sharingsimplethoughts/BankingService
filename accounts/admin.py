from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ['id','name','username','email','mobile'] 
    list_display = ['id','name','username','email','mobile','user_type','created_on','last_signin'] 
    readonly_fields = ['created_on','last_signin','username','email','mobile','user_type','name']

class UserAccountAdmin(admin.ModelAdmin):
	search_fields = ['user__name','user__username','user__email','user__mobile']
	list_display = ['id','user__name','balance']
	readonly_fields = ['balance','updated_on']

admin.site.register(User,UserAdmin)
admin.site.register(UserAccount)