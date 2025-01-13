from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from io import BytesIO
import qrcode
import base64

class LoginView(View):
    template_name = 'accounts/login.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:2fa')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, self.template_name)
        
class TwoFactorAuthView(View, LoginRequiredMixin):
    template_name = 'accounts/2fa-login.html'

    def get(self, request):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device or not device.confirmed:
            return redirect('accounts:2fa-register')
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        device = get_user_totp_device(self, user)
        if device.verify_token(request.POST['token']):
            return redirect('app:home')
        else:
            messages.error(request, 'Invalid token')
            return render(request, self.template_name)
        
class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # Create user
        user = User.objects.create_user(username, email, password)
        if user:
            user.save()
            return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, self.template_name)
    
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
            return redirect('app:home')
        print(dir(device))
        qr_code = qrcode.make(device.config_url)
        qr_code = get_base64_encoded_image(qr_code)
        return render(request, self.template_name, {'qr_code': qr_code})
    
    def post(self, request):
        user = request.user
        device = get_user_totp_device(self, user)
        if device and not device.confirmed:
            if device.verify_token(request.POST['token']):
                device.confirmed = True
                device.save()
                return redirect('app:home')
            else:
                messages.error(request, 'Invalid token')
                return render(request, self.template_name)
        return redirect('app:home')
    
def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
    return user.totpdevice_set.create(confirmed=False)

def get_base64_encoded_image(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()