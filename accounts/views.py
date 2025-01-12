from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.views import View

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
            return redirect('2fa')
        else:
            return redirect('login')
        
class TwoFactorAuthView(View):
    template_name = 'accounts/2fa.html'

    @login_required
    def get(self, request):
        return render(request, self.template_name)
    
    @login_required
    def post(self, request):
        return redirect('home')
    
class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        return redirect('login')
    
class RecoverPasswordView(View):
    template_name = 'accounts/recover_password.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        return redirect('login')