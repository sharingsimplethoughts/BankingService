from transaction.models import Transaction
from .models import User
import string
import random
import requests
from django.conf import settings

access_key = settings.CURRENCY_CONVERT_KEY

def generatetid(x):
    t = Transaction.objects.all().order_by('-id').first()
    id = int(t.id)+1 if t else 1
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = x))
    print(res[:5]+str(id)+res[6:])
    return res[:5]+str(id)+res[6:]


def get_currency_rates():
    url = str.__add__('http://data.fixer.io/api/latest?access_key=', access_key)  
    data = requests.get(url).json()
    rates = data["rates"]
    return rates
    
def convert(from_currency,amount,rates,to_currency='INR'):
    if from_currency != 'EUR':
            amount = amount / rates[from_currency]
    amount = round(amount * rates[to_currency], 2)
    return amount

def send_email(email):
    pass

def generate_excel(id=''):
    pass
