from django.conf import settings
from django.forms.utils import ErrorList
from django.contrib.auth import get_user_model
User = get_user_model()

def validate_username(username, form) -> ErrorList | None:
    errors = ErrorList()
    if User.objects.filter(username=username).exists():
        # form.add_error('username', 'You cannot use this username')
        errors.append('You cannot use this username')
    if not all(char in settings.USERNAME_ALLOWED_CHARS for char in username):
        form.add_error('username', 'Username contains invalid characters')

    return errors or None

def validate_password(password, form) -> ErrorList | None:
    errors = ErrorList()
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    if all(char.isdigit() for char in password):
        errors.append('Password must contain at least one letter')
    if all(char.isalpha() for char in password):
        errors.append('Password must contain at least one number')

    return errors or None