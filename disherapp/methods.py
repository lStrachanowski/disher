from django.contrib.auth.models import User

def check_if_user_is_logged():
    user_is_logged = False
    return user_is_logged

def check_user(username):
    if User.objects.filter(username= username).exists():
        return True
    else:
        return False
