from django_otp.decorators import otp_required
from .models import Note
from django.views import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from .forms import NoteForm
from django.contrib import messages
from .helpers import encrypt_content, decrypt_content
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes
from .models import BlockedIP

User = get_user_model()

@method_decorator(otp_required, name='dispatch')
class HomeView(View):
    template_name = 'app/home.html'

    def get(self, request):
        public_notes = Note.objects.filter(is_public=True)
        shared_notes = Note.objects.filter(shared_with=request.user)
        user_notes = Note.objects.filter(user=request.user)
        context = {
            'public_notes': public_notes,
            'shared_notes': shared_notes,
            'user_notes': user_notes
        }
        return render(request, self.template_name, context)

@method_decorator(otp_required, name='dispatch')
class AddNoteView(View):
    template_name = 'app/add_note.html'
    
    def get(self, request):
        form = NoteForm()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = NoteForm(request.POST)
        if not form.is_valid():
            for error in form.errors:
                messages.error(request, form.errors[error])
            return render(request, self.template_name, {'form': form})
        content = form.cleaned_data['content']

        recipient_names = form.cleaned_data['shared_with'].split(',')
        if len(recipient_names) > 10 or len(recipient_names) < 1:
            messages.error(request, 'You can only share notes with up to 10 recipients')
            return render(request, self.template_name, {'form': form})
        
        for recipient_name in recipient_names:
            if not all(char in settings.USERNAME_ALLOWED_CHARS for char in recipient_name):
                messages.error(request, 'Invalid recipient names')
                return render(request, self.template_name, {'form': form})

        recipients = User.objects.filter(username__in=recipient_names)


        encrypted = form.cleaned_data['is_encrypted']
        password = form.cleaned_data['password']
        if encrypted and not password:
            messages.error(request, 'Password is required for encrypted notes')
            return render(request, self.template_name, {'form': form})
        if encrypted:
            encrypted_content, key = encrypt_content(content, password)
            note = Note.objects.create(user=request.user,
                                title=form.cleaned_data['title'],
                                content=encrypted_content,
                                is_public=form.cleaned_data['is_public'],
                                is_encrypted=True,
                                password=key,)
        else:
            note = Note.objects.create(user=request.user,
                                title=form.cleaned_data['title'],
                                content=content,
                                is_public=form.cleaned_data['is_public'],\
                                is_encrypted=False,
                                password=None,)
        note.shared_with.set(recipients)
        return redirect('app:home')

@otp_required
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def password_confirm(request):
    user = request.user
    password = request.data.get('password')
    note_id = request.data.get('note_id')
    if not password or not note_id:
        return Response({'error': 'Invalid request'}, status=400)
    note = Note.objects.get(id=request.data['note_id'])
    if not note.is_accessible(user):
        return Response({'error': 'Unauthorized'}, status=403)
    if not note.is_encrypted:
        return Response({'error': 'Note is not encrypted'}, status=400)
    if not note.verify_password(password):
        return Response({'error': 'Invalid password'}, status=400)
    note.content = decrypt_content(note.content, password)
    return Response({'content': note.content})

def honeypot_admin(request):
    ip_address = request.META.get('REMOTE_ADDR')
    BlockedIP.objects.create(ip=ip_address, offense='Trying to access admin page')
    return redirect('app:home')