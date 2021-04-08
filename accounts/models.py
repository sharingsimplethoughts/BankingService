from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
device_type_choices=(('1','Android'),('2','Ios'),('3','Web'))
user_type_choices=(('1','User'),('2','Manager'),('3','Admin'))

class User(AbstractUser):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=200,blank=True,null=True)
    profile_image = models.ImageField(upload_to='user/profile_image',blank=True,null=True)
    mobile = models.CharField(max_length=200,blank=True,null=True)

    lat = models.CharField(max_length=50,blank=True,null=True)
    lon = models.CharField(max_length=50,blank=True,null=True)

    device_type = models.CharField(max_length=10,choices=device_type_choices)
    device_token = models.CharField(max_length=200,blank=True,null=True)
    user_type = models.CharField(max_length=20,choices=user_type_choices)

    has_dual_account = models.BooleanField(default=False)

    is_mail_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    
    is_deleted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    is_notification_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    last_signin = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.username

class UserAccount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ua_user')
    balance = models.DecimalField(max_digits=20,decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return str(self.id)
