from django import forms

class RegisterForm(forms.Form):
    user_name = forms.CharField(label="Your name", max_length=100)
    user_email = forms.EmailField()
    user_password =  forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_user_password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class LoginForm(forms.Form):
    user_name = forms.CharField(label="Your name", max_length=100)
    user_password =  forms.CharField(max_length=32, widget=forms.PasswordInput)

class ResetForm(forms.Form):
    user_email = forms.EmailField() 