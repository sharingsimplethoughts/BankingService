from transaction.models import Transaction
from .models import User
import string
import random
import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

access_key = settings.CURRENCY_CONVERT_KEY

def generatetid(x):
    t = Transaction.objects.all().order_by('-id').first()
    id = int(t.id)+1 if t else 1
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = x))
    return res[:5]+str(id)+res[6:]


def get_currency_rates():
    url = str.__add__('http://data.fixer.io/api/latest?access_key=', access_key)  
    data = requests.get(url).json()
    rates = data["rates"]
    return rates
    
def convert(from_currency,amount,rates,to_currency='INR'):
    if from_currency != 'EUR':
            amount = float(amount) / rates[from_currency]
    amount = round(amount * rates[to_currency], 2)
    return amount

def send_email(to_email,amount,type,balance):
    try:
        subject, from_email, to = 'Notification', 'DemoBankService <webmaster@localhost>', to_email
        text_content = 'This is a notification'
        html_content = '<p>Rs.<strong> '+str(amount)+' deposited</strong> in your account. Your balance is Rs.<strong> '+str(balance)+' </strong>.</p>'
        if type=="1":
            html_content = '<p>Rs.<strong> '+str(amount)+' withdrawn</strong> from your account. Your balance is Rs.<strong> '+str(balance)+' </strong>.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except:
        return False