from django.urls import path
from .views import HomeView, AddNoteView, password_confirm

app_name = 'app'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('', HomeView.as_view()),
    path('add-note/', AddNoteView.as_view(), name='add-note'),
    path('api/password-confirm/', password_confirm, name='password-confirm'),
]