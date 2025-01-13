from django.urls import re_path, path
from . import api
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^api/user/totp/create/$', api.TOTPCreateView.as_view(), name='api-totp-create'),
    re_path(r'^api/user/totp/login/(?P<token>[0-9]{6})/$', api.TOTPVerifyView.as_view(), name='api-totp-login'),
    path('api/user/register/', api.register_user, name='api-register'),
    path('api/user/login/', api.user_login, name='api-login'),
    path('logout/', api.user_logout, name='api-logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('recover-password/', views.RecoverPasswordView.as_view(), name='recover-password'),
    path('login/2fa/', views.TwoFactorAuthView.as_view(), name='2fa'),
    path('login/2fa/register/', views.TwoFactorAuthRegisterView.as_view(), name='2fa-register'),
]