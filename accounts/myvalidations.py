

def validate_email(email):
    if '@' not in email:
        return False
    else:
        temp_email = email.split('@')[1]
        if '.' not in temp_email:
            return False
        t_email = temp_email.split('.')
        if len(t_email) <2:
            return False
        if temp_email.split('.')[1]=='':
            return False
    if len(email)<9 or len(email)>50:
        return False
    return True

def validate_password(password):
    return not (len(password)<8 or len(password)>20)

def validate_mobile(mobile):
    if not mobile.isdigit():
        return False
    if len(mobile)<10 or len(mobile)>15:
        return False
    return True

def validate_name(name):
    if any(c.isdigit() for c in name):
        return False
    if len(name)<3 or len(name)>50:
        return False
    return True

def validate_username(username):
    return not (len(username)<8 or len(username)>20)

def validate_initial_deposit(amount):
    return not len(str(round(float(amount),2)))>20

def validate_amount(amount):
    return not len(str(round(float(amount),2)))>20
