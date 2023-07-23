from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        label="Your name", min_length=3, max_length=100, required=True)
    user_email = forms.EmailField(required=True)
    user_password = forms.CharField(
        min_length=6, max_length=32, widget=forms.PasswordInput, required=True)
    confirm_user_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput, required=True)

class LoginForm(forms.Form):
    user_name = forms.CharField(label="Your name", min_length=3, max_length=100,
                                required=True, error_messages={'required': 'Enter your name'})
    user_password = forms.CharField(
        min_length=6, max_length=32, widget=forms.PasswordInput, required=True, error_messages={'required': ''})


class ResetForm(forms.Form):
    user_email = forms.EmailField(required=True)