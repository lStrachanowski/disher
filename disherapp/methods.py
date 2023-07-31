from django.contrib.auth.models import User

class CheckIfUserIsLogged:   
    def set_user_status_to_logged(self,request):
            request.session['is_logged'] = True
    def get_user_status(self,request):
        if request.session.get('is_logged'):
            status = request.session['is_logged']
            return status
        else:
            request.session['is_logged'] = False

class Logout_user:
    def logout(self,request):
        request.session['is_logged'] = False

# Checks if username exist
def check_user(username):
    status = User.objects.filter(username = username).exists()
    return status

# Checks if user email exist
def check_email(email):
     status = User.objects.filter(email = email).exists()
     return status

# Is activating accoutnt
def activate_email(email):
    user = User.objects.get(email = email)
    user.is_active = True
    user.save() 

# Is reseting user password
def reset_password(email, password):
     user = User.objects.get(email = email)
     user.set_password(password)
     user.save() 