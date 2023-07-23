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

def check_user(username):
    status = User.objects.filter(username = username).exists()
    return status
