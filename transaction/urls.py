from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'tran'

urlpatterns = [
	path('transaction',TransactionView.as_view(),name='transaction'),
	path('enquiry',EnquiryView.as_view(),name='enquiry'),
	path('single_transaction_history',THistorySingleView.as_view(),name='single_transaction_history'),
	path('all_transaction_history',THistoryAllView.as_view(),name='all_transaction_history'),
]