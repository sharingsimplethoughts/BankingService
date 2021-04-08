from rest_framework import serializers
from datetime import datetime
import pytz
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import APIException
from django.db import transaction
from .models import *
from transaction.models import *
from .myvalidations import *
from .extra_functions import *

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class RegisterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True)
    username = serializers.CharField(allow_blank=True)
    email = serializers.CharField(allow_blank=True)
    mobile = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True)
    profile_image = serializers.ImageField(required=False)
    lat = serializers.CharField(allow_blank=True)
    lon = serializers.CharField(allow_blank=True)
    
    device_type = serializers.CharField(allow_blank=True)
    device_token = serializers.CharField(allow_blank=True)
    user_type = serializers.CharField(allow_blank=True)

    initial_deposit = serializers.CharField(allow_blank=True)
    payment_mode = serializers.CharField(allow_blank=True)
    
    uid = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    is_mobile_verified = serializers.CharField(read_only=True)
    has_dual_account = serializers.CharField(read_only=True)
    transaction_id = serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=('name','username','email','mobile','password','profile_image','lat','lon',
                'device_type','device_token','user_type','initial_deposit','payment_mode',
                'uid','token','is_mobile_verified','has_dual_account','transaction_id')

    def validate(self,data):
        name = data['name']
        username = data['username']
        email = data['email']
        mobile = data['mobile']
        password = data['password']
        lat = data['lat']
        lon = data['lon']
        device_type = data['device_type']
        device_token = data['device_token']
        user_type = data['user_type']
        initial_deposit = data['initial_deposit']
        payment_mode = data['payment_mode']

        if not name or name=="":
            raise APIException({
                'success':'False',
                'message':'Please provide name',
            })
        if not username or username=="":
            raise APIException({
                'success':'False',
                'message':'Please provide username',
            })
        if not email or email=="":
            raise APIException({
                'success':'False',
                'message':'Please provide email',
            })
        if not mobile or mobile=="":
            raise APIException({
                'success':'False',
                'message':'Please provide mobile',
            })
        if not password or password=="":
            raise APIException({
                'success':'False',
                'message':'Please provide password',
            })
        if not lat or lat=="":
            raise APIException({
                'success':'False',
                'message':'Please provide lat',
            })
        if not lon or lon=="":
            raise APIException({
                'success':'False',
                'message':'Please provide lon',
            })
        if not device_type or device_type=="":
            raise APIException({
                'success':'False',
                'message':'Please provide device type',
            })
        if not device_token or device_token=="":
            raise APIException({
                'success':'False',
                'message':'Please provide device token',
            })
        if not user_type or user_type=="":
            raise APIException({
                'success':'False',
                'message':'Please provide user type',
            })
        if not initial_deposit or initial_deposit=="":
            raise APIException({
                'success':'False',
                'message':'Please provide initial deposit amount(Rs)',
            })
        if not payment_mode or payment_mode=="":
            raise APIException({
                'success':'False',
                'message':'Please provide payment_mode',
            })

        if not validate_name(name):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid name',
            })
        if not validate_username(username):
            raise APIException({
                'success':'False',
                'message':'Username is not valid',
            })
        u = User.objects.filter(username=username).first()
        if u:
            raise APIException({
                'message':'Username already exists',
                'success':'False'
            })

        if not validate_email(email):
        	raise APIException({
                'success':'False',
                'message':'Email id is invalid',
            })
        user=User.objects.filter(email=email,user_type=user_type).first()
        if user:
            raise APIException({
                'success':'False',
                'message':'Email id is already registered',
            })
        
        if not validate_mobile(mobile):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid mobile',
            })
        
        if not validate_password(password):
            raise APIException({
                'success':"False",
                'message':'Password is not valid',
            })

        if device_type not in ('1','2','3'):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid device type',
            })
        
        if user_type not in ('1','2','3'):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid user type',
            })

        if not validate_initial_deposit(initial_deposit):
            raise APIException({
                'success':'False',
                'message':'Initial deposit amont is not valid',
            })
        if payment_mode not in ('1','2'):
            raise APIException({
                'success':'False',
                'message':'Please provide valid payment_mode',
            })

        
        return data

    def create(self,validated_data):
        name = validated_data['name']
        username = validated_data['username']
        email = validated_data['email']
        mobile = validated_data['mobile']
        password = validated_data['password']
        lat = validated_data['lat']
        lon = validated_data['lon']
        device_type = validated_data['device_type']
        device_token = validated_data['device_token']
        user_type = validated_data['user_type']
        profile_image = self.context['request'].FILES.get('profile_image')
        initial_deposit = validated_data['initial_deposit']
        payment_mode = validated_data['payment_mode']

        x = User.objects.filter(email=email).count()
        has_dual_account = True if x else False
        
        with transaction.atomic():
            user=User(
                name = name,
                username = username,
                email = email,
                mobile = mobile,
                lat = lat,
                lon = lon,
                device_type = device_type,
                device_token = device_token,
                user_type = user_type,
                profile_image = profile_image,
                has_dual_account = has_dual_account,
            )
            user.save()

            user.set_password(password)
            user.save()

            ua = UserAccount(
                user = user,
                balance = round(float(initial_deposit),2)
            )
            ua.save()

            t = Transaction(
                tid = generatetid(10),
                user_account = ua,
                earlier_balance = 0.00,
                amount = ua.balance,
                new_balance = ua.balance,
                transaction_mode = "1",
                payment_mode = payment_mode,
                payment_status = "1",
            )
            t.save()

        validated_data['uid']=user.id
        validated_data['has_dual_accounts']=user.has_dual_account
        validated_data['transaction_id']=t.tid

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        token = 'JWT '+token

        validated_data['token'] = token

        return validated_data

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True)
    device_type = serializers.CharField(allow_blank=True)
    device_token = serializers.CharField(allow_blank=True)
    user_type = serializers.CharField(allow_blank=True)

    uid = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    has_dual_account = serializers.CharField(read_only=True)
    profile_image = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    balance = serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=('username','password','device_type','device_token','user_type','uid',
            'token','has_dual_account','profile_image','name','email','balance')

    def validate(self,data):
        username=data['username']
        password=data['password']
        device_type=data['device_type']
        device_token=data['device_token']
        user_type=data['user_type']

        if not username or username=="":
            raise APIException({
                'success':'False',
                'message':'Please provide username',
            })
        if not password or password=='':
            raise APIException({
                'success':'False',
                'message':'Password is required',
            })
        if not device_type or device_type=='':
            raise APIException({
                'success':'False',
                'message':'Device_type is required',
            })
        if not device_token or device_token=='':
            raise APIException({
                'success':'False',
                'message':'Device token is required',
            })
        if not user_type or user_type=='':
            raise APIException({
                'success':'False',
                'message':'Please provide user_type',
            })

        
        if not validate_username(username):
            raise APIException({
                'success':'False',
                'message':'Please provide valid username',
            })
        if not validate_password(password):
            raise APIException({
                'success':"False",
                'message':'Password is not valid',
            })

        if device_type not in ['1','2','3']:
            raise APIException({
                'success':'False',
                'message':'Please enter correct format of device_type',
            })

        if user_type not in ['1','2']:
            raise APIException({
                'success':'False',
                'message':'Value of user_type key must be either 1 or 2',
            })
        
        user = User.objects.filter(username=username,user_type=user_type).first()
        
        if user:
            if not user.check_password(password):
                raise APIException({
                    'success':'False',
                    'message':'Invalid password',
                })
        else:
            raise APIException({
                'success':'False',
                'message':'May be your username or password is wrong1',
            })

        if user.is_blocked:
            raise APIException({
                'success':'False',
                'message':'Your account has been blocked',
            })
        if user.is_deleted:
            raise APIException({
                'success':'False',
                'message':'May be your username or password is wrong2',
            })

        now=datetime.utcnow().replace(tzinfo=pytz.utc)

        user.device_type = device_type
        user.device_token = device_token
        user.last_signin = now
        user.save()

        data['uid'] = user.id
        data['password'] = ''
        data['has_dual_account'] = user.has_dual_account
        data['profile_image'] = ''
        if user.profile_image:
            data['profile_image'] = user.profile_image.url
        data['name'] = user.name
        data['email'] = user.email
        data['balance'] = user.ua_user.first().balance

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        token = 'JWT '+token
        data['token'] = token

        return data

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','email','mobile')