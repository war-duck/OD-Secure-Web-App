from django.urls import path
from .views import home

app_name = 'app'
urlpatterns = [
    path('home/', home, name='home'),
    path('', home),
]