from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django_otp import devices_for_user, login as login_otp
from django_otp.plugins.otp_totp.models import TOTPDevice
from io import BytesIO
import qrcode
import base64
from .forms import RegisterForm, LoginForm, TwoFactorAuthForm
User = get_user_model()

class LoginView(View):
    template_name = 'accounts/login.html'
    
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            for error in form.errors:
                messages.error(request, form.errors[error])
            return render(request, self.template_name, {'form': form})
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            clear_messages(request)
            return redirect('accounts:2fa')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, self.template_name, {'form': form})

class TwoFactorAuthView(View, LoginRequiredMixin):
    template_name = 'accounts/2fa-login.html'

    def get(self, request):
        form = TwoFactorAuthForm()
        user = request.user
        device = get_user_totp_device(self, user)
        if not device or not device.confirmed:
            return redirect('accounts:2fa-register')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        tokenForm = TwoFactorAuthForm(request.POST)
        if not tokenForm.is_valid():
            for error in tokenForm.errors:
                messages.error(request, tokenForm.errors[error])
            device = get_user_totp_device(self, user)
            if not device or not device.confirmed:
                return redirect('accounts:2fa-register')
            return render(request, self.template_name, {'form': tokenForm})
        device = get_user_totp_device(self, user)
        if device.verify_token(tokenForm.cleaned_data['token']):
            login_otp(request, device)
            clear_messages(request)
            return redirect('app:home')
        else:
            messages.error(request, 'Invalid token')
            device = get_user_totp_device(self, user)
            if not device or not device.confirmed:
                return redirect('accounts:2fa-register')
            qrcode = get_base64_encoded_qr_code(device.config_url)
            return render(request, self.template_name, {'form': tokenForm})
        
class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            for error in form.errors:
                messages.error(request, form.errors[error])
            return render(request, self.template_name, {'form': form})
        cleaned_data = form.clean()
        user = User.objects.create_user(username=cleaned_data['username'], password=cleaned_data['password'])
        if user:
            user.save()
            login(request, user)
            clear_messages(request)
            return redirect('accounts:2fa-register')
        else:
            messages.error(request, 'Something went wrong')
            return render(request, self.template_name, {'form': form})
    
class RecoverPasswordView(View):
    template_name = 'accounts/recover-password.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        return redirect('accounts:login')
    
class TwoFactorAuthRegisterView(View, LoginRequiredMixin):
    template_name = 'accounts/2fa-register.html'

    def get(self, request):
        user = request.user
        device = get_user_totp_device(self, user)
        if device and device.confirmed:
            return redirect('accounts:2fa')
        qr_code = get_base64_encoded_qr_code(device.config_url)
        return render(request, self.template_name, {'qr_code': qr_code, 'form': TwoFactorAuthForm()})
    
    def post(self, request):
        user = request.user
        tokenForm = TwoFactorAuthForm(request.POST)
        if not tokenForm.is_valid():
            for error in tokenForm.errors:
                messages.error(request, tokenForm.errors[error])
            device = get_user_totp_device(self, user)
            qr_code = get_base64_encoded_qr_code(device.config_url)
            return render(request, self.template_name, {'qr_code': qr_code, 'form': tokenForm})
        device = get_user_totp_device(self, user)
        if device and not device.confirmed:
            if device.verify_token(tokenForm.cleaned_data['token']):
                device.confirmed = True
                device.save()
                clear_messages(request)
                return redirect('app:home')
            else:
                messages.error(request, 'Invalid token')
                device = get_user_totp_device(self, user)
                qr_code = get_base64_encoded_qr_code(device.config_url)
                return render(request, self.template_name, {'qr_code': qr_code, 'form': tokenForm})
        login_otp(request, device)
        return redirect('app:home')
    
def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
    return user.totpdevice_set.create(confirmed=False)

def get_base64_encoded_qr_code(url):
    image = qrcode.make(url)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def clear_messages(request):
    storage = messages.get_messages(request)
    for message in storage:
        pass