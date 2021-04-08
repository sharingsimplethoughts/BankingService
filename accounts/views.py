from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from django.db import transaction
from .models import *
from .serializers import *

# Create your views here.

class RegisterUserView(APIView):
    def post(self,request,*args,**kwargs):
        # try:
        serializer=RegisterUserSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success':'True',
                'message':'Registration successfull',
                'data':serializer.data,
            },200)
        return Response({
            'success':'False',
            'message':serializer.errors,
        },400)
        # except APIException as e:
        #     raise e
        # except Exception as e:
        #     return Response({
        #         'success':'False',
        #         'message':'Registration was unsuccessfull',
        #     },400)

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,*args,**kwargs):
        try:
            data=request.data
            serializer=LoginSerializer(data=data,context={'request':request})
            if serializer.is_valid():
                data=serializer.data
                return Response({
                    'success':'True',
                    'message':'Data retrieved successfully',
                    'data':data
                },status=200)
            
            return Response({
                'success':'False',
                'message': serializer.errors,
            },status=400)
        except APIException as e:
            raise e
        except Exception as e:
            return Response({
                'success':'False',
                'message':str(e),
            },400)