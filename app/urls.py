from django.urls import path
from .views import home
# from .views import home, custom_login_view, custom_two_factor_view
from django.urls import include
from two_factor.urls import urlpatterns as tf_urls

app_name = 'app'
urlpatterns = [
    path('home/', home, name='home'),
    path('', home),
    path('', include(tf_urls)),
]