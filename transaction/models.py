from django.db import models
from accounts.models import *
# Create your models here.

transaction_mode_choices = (('1','Credit'),('2','Debit'))
payment_mode_choices = (('1','Cash'),('2','Online'))
payment_status_choices = (('1','Success'),('2','Failed'))

class Transaction(models.Model):
	tid = models.CharField(max_length=20)
	user_account = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='t_user')
	earlier_balance = models.DecimalField(max_digits=20,decimal_places=2, default=0.00)
	amount = models.DecimalField(max_digits=15,decimal_places=2, default=0.00)
	new_balance = models.DecimalField(max_digits=20,decimal_places=2, default=0.00)
	transaction_mode = models.CharField(max_length=10,choices=transaction_mode_choices)
	payment_mode = models.CharField(max_length=10,choices=payment_mode_choices)
	payment_status = models.CharField(max_length=10,choices=payment_status_choices,default='2')
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.tid




