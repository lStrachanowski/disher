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

class ResetPasswordForm(forms.Form):
    user_password = forms.CharField(
        min_length=6, max_length=32, widget=forms.PasswordInput, required=True)
    confirm_user_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput, required=True)


class DishForm(forms.Form):
    dish_title = forms.CharField( min_length=3, max_length=100, required=True)
    # dish_calories = forms.IntegerField( required=True)
    dishDescription = forms.CharField( max_length=1000, required=True)
    duration = forms.CharField( min_length=1, max_length=100, required=True)
    type_of_meal = forms.CharField( min_length=1, max_length=100, required=True)


class ChangePassword(forms.Form):
    current_password = forms.CharField(
        min_length=6, max_length=32, widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput, required=True)
    new_password_confirmation = forms.CharField(
        max_length=32, widget=forms.PasswordInput, required=True)

class ChangeUserName(forms.Form):
    user_name = forms.CharField(
        min_length=3, max_length=32, widget=forms.PasswordInput, required=True)
    new_user_name = forms.CharField(min_length=3,
        max_length=32, widget=forms.PasswordInput, required=True)
    user_password = forms.CharField(min_length=3,
        max_length=32, widget=forms.PasswordInput, required=True)

class ChangeEmail(forms.Form):
    user_email = forms.EmailField(required=True)
    new_user_email = forms.EmailField(required=True)
    user_password = forms.CharField(min_length=3,
    max_length=32, widget=forms.PasswordInput, required=True)

