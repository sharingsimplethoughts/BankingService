from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'accounts'

urlpatterns = [
	path('register',RegisterUserView.as_view(),name='register'),
	path('login',LoginView.as_view(),name='login'),
]