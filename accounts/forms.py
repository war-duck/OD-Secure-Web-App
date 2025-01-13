from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'You cannot use this username')
        if len(password) < 8:
            self.add_error('password', 'Password must be at least 8 characters long')
        if not all(char in settings.USERNAME_ALLOWED_CHARS for char in username):
            self.add_error('username', 'Username contains invalid characters')
        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
class TwoFactorAuthForm(forms.Form):
    token = forms.CharField(max_length=6)
    
    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data.get('token')
        if not token.isdigit():
            self.add_error('token', 'Token must be a number')
        return cleaned_data