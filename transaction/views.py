from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from django.db import transaction
from .models import *
from .serializers import *
from accounts.myvalidations import *
from accounts.extra_functions import *

from datetime import datetime
from django.utils.timezone import utc
import pytz

from rest_framework.renderers import JSONRenderer
from drf_renderer_xlsx.renderers import XLSXRenderer
from drf_renderer_xlsx.mixins import XLSXFileMixin
# Create your views here.


class TransactionView(APIView):
	permission_classes=[IsAuthenticated,]
	authentication_classes=[JSONWebTokenAuthentication,]
	def patch(self,request,*args,**kwargs):
		try:
			user = request.user
			amount = request.data['amount']
			from_currency = request.data['from_currency']
			transaction_mode = request.data['transaction_mode']
			payment_mode = request.data['payment_mode']

			rates = get_currency_rates()
			currency_list = list(rates.keys())

			if not amount or amount=="":
				return Response({
					'message':'Please provide amount',
					'success':'False',
				},400)
			if not from_currency or from_currency=="":
				return Response({
					'message':'Please provide from_currency',
					'success':'False',
				},400)
			if from_currency not in currency_list:
				return Response({
					'message':'Please provide a valid from_currency',
					'success':'False',
				},400)
			if not transaction_mode or transaction_mode=="":
				return Response({
					'message':'Please provide transaction_mode',
					'success':'False'
				},400)
			if transaction_mode not in ('1','2'):
				return Response({
					'message':'Please provide a valid transaction_mode',
					'success':'False'
				},400)
			if not payment_mode or payment_mode=="":
				return Response({
					'message':'Please provide payment_mode',
					'success':'False'
				},400)
			if payment_mode not in ('1','2'):
				return Response({
					'message':'Please provide valid payment_mode',
					'success':'False'
				},400)

			amount = convert(from_currency,amount,rates)
			now=datetime.utcnow().replace(tzinfo=utc)

			ua = user.ua_user.first()

			with transaction.atomic():
				earlier_balance = ua.balance

				if transaction_mode == '1':
					ua.balance = round(float(ua.balance)+float(amount),2)
				else:
					if ua.balance < amount:
						return Response({
							'message':'Insufficient balance',
							'success':'False',
						},400)
					ua.balance = round(float(ua.balance)-float(amount),2)

				ua.updated_on = now
				ua.save()

				t = Transaction(
					tid = generatetid(10),
					user_account = ua,
					earlier_balance = earlier_balance,
					amount = float(amount),
					new_balance = ua.balance,
					transaction_mode = transaction_mode,
					payment_mode = payment_mode,
					payment_status = "1",
				)
				t.save()

			res = send_email(user.email,amount,transaction_mode,ua.balance)

			serializer = GetTransactionDetailSerializer(t)

			return Response({
				'message':'Transaction successfull',
				'success':'True',
				'data':serializer.data
			},200)

		except Exception as e:
			return Response({
				'success':'False',
				'message':'Internal server error',
			},400)


class EnquiryView(APIView):
	permission_classes=[IsAuthenticated,]
	authentication_classes=[JSONWebTokenAuthentication,]
	def get(self,request,*args,**kwargs):
		try:
			serializer = GetEnquiryDetailSerializer(request.user)
			return Response({
				'message':'Data retrieved successfully',
				'success':'True',
				'data':serializer.data
			},200)
		except Exception as e:
			return Response({
				'success':'False',
				'message':'Internal server error',
			},400)

class THistorySingleView(APIView):
	permission_classes=[IsAuthenticated,]
	authentication_classes=[JSONWebTokenAuthentication,]
	renderer_classes = [JSONRenderer, XLSXRenderer, XLSXFileMixin]
	def get(self,request,*args,**kwargs):
		try:
			mngr = request.user
			if mngr.user_type != '2':
				return Response({
					'message':'Only managers can send this request',
					'success':'False'
				},400)
			
			id = request.GET['id']
			st_date = request.GET['st_date']
			end_date = request.GET['end_date']
			now=datetime.utcnow().replace(tzinfo=pytz.utc)

			if not id or  id=="":
				return Response({
					'message':'Please provide user id',
					'success':'False',
				},400)
			user = User.objects.filter(id=id).exclude(id=mngr.id).first()
			if not user:
				return Response({
					'message':'Please provide a valid user id',
					'success':'False'
				},400)
			if not st_date or st_date=="":
				return Response({
					'message':'Please provide st_date',
					'success':'False',
				},400)
			if not end_date or end_date=="":
				return Response({
					'message':'Please provide end_date',
					'success':'False',
				},400)
			try:
				st_date = datetime.strptime(st_date, "%Y-%m-%d")
			except:
				return Response({
					'message':'Please provide a valid st_date',
					'success':'False',
				},400)
			st_date = st_date.replace(tzinfo=pytz.utc)
			if st_date > now:
				return Response({
					'message':'Start date can not be greater then today',
					'success':'False',
				},400)
			try:
				end_date = datetime.strptime(end_date, "%Y-%m-%d")
				end_date = end_date.replace(hour=23, minute=59)
			except:
				return Response({
					'message':'Please provide a valid end_date',
					'success':'False',
				},400)
			end_date = end_date.replace(tzinfo=pytz.utc)

			if st_date>end_date:
				return Response({
					'message':'Start date can not be greater than end date',
					'success':'False',
				},400)

			serializer = GetEnquiryDetailSerializer(user,context={'st_date':st_date,'end_date':end_date})
			return Response({
				'message':'Data retrieved successfully',
				'success':'True',
				'data':serializer.data
			},200)
		except Exception as e:
			return Response({
				'success':'False',
				'message':'Internal server error',
			},400)


class THistoryAllView(APIView):
	permission_classes=[IsAuthenticated,]
	authentication_classes=[JSONWebTokenAuthentication,]
	renderer_classes = [JSONRenderer, XLSXRenderer, XLSXFileMixin]
	def get(self,request,*args,**kwargs):
		try:
			mngr = request.user
			if mngr.user_type != '2':
				return Response({
					'message':'Only managers can send this request',
					'success':'False'
				},400)
			
			st_date = request.GET['st_date']
			end_date = request.GET['end_date']
			now=datetime.utcnow().replace(tzinfo=pytz.utc)

			if not st_date or st_date=="":
				return Response({
					'message':'Please provide st_date',
					'success':'False',
				},400)
			if not end_date or end_date=="":
				return Response({
					'message':'Please provide end_date',
					'success':'False',
				},400)
			try:
				st_date = datetime.strptime(st_date, "%Y-%m-%d")
			except:
				return Response({
					'message':'Please provide a valid st_date',
					'success':'False',
				},400)
			st_date = st_date.replace(tzinfo=pytz.utc)
			if st_date > now:
				return Response({
					'message':'Start date can not be greater then today',
					'success':'False',
				},400)
			try:
				end_date = datetime.strptime(end_date, "%Y-%m-%d")
				end_date = end_date.replace(hour=23, minute=59)
			except:
				return Response({
					'message':'Please provide a valid end_date',
					'success':'False',
				},400)
			end_date = end_date.replace(tzinfo=pytz.utc)

			if st_date>end_date:
				return Response({
					'message':'Start date can not be greater than end date',
					'success':'False',
				},400)

			queryset = User.objects.all().exclude(id=request.user.id,is_superuser=True)
			serializer = GetEnquiryDetailSerializer(queryset,many=True,context={'st_date':st_date,'end_date':end_date})
			return Response({
				'message':'Data retrieved successfully',
				'success':'True',
				'data':serializer.data
			},200)
		except Exception as e:
			return Response({
				'success':'False',
				'message':'Internal server error',
			},400)