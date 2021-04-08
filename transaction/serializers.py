from rest_framework import serializers
from datetime import datetime
from .models import *
from accounts.models import *
from accounts.serializers import UserDetailSerializer


class GetEnquiryDetailSerializer(serializers.ModelSerializer):
	user_detail = serializers.SerializerMethodField()
	transaction_detail = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ('user_detail','transaction_detail')
	
	def get_user_detail(self,instance):
		serializer = UserDetailSerializer(instance)
		return serializer.data
	def get_transaction_detail(self,instance):
		st_date = self.context.get('st_date')
		end_date = self.context.get('end_date')
		if st_date and end_date:
			queryset = Transaction.objects.filter(user_account__user=instance,created_on__range=(st_date,end_date))
		else:
			queryset = Transaction.objects.filter(user_account__user=instance)
		serializer = GetTransactionDetailSerializer(queryset,many=True)
		return serializer.data


class GetTransactionDetailSerializer(serializers.ModelSerializer):
	transaction_mode = serializers.CharField(source='get_transaction_mode_display')
	payment_mode = serializers.CharField(source='get_payment_mode_display')
	payment_status = serializers.CharField(source='get_payment_status_display')
	created_on = serializers.SerializerMethodField()
	class Meta:
		model = Transaction
		fields = ('tid','earlier_balance','amount','new_balance','transaction_mode',
			'payment_mode','payment_status','created_on')

	def get_created_on(self,instance):
		created_on = datetime.timestamp(instance.created_on)
		return int(created_on)
