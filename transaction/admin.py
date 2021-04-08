from django.contrib import admin
from .models import *
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['id','tid','amount','transaction_mode','payment_mode','payment_status'] 
    list_display = ['id','tid','amount','transaction_mode','payment_mode','payment_status'] 
    readonly_fields = ['created_on','tid','amount','transaction_mode','payment_mode','payment_status']

admin.site.register(Transaction,TransactionAdmin)