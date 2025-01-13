from django_otp.decorators import otp_required
from .models import Note
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from .forms import NoteForm
from django.contrib import messages
from .helpers import encrypt_content, decrypt_content

@method_decorator(otp_required, name='dispatch')
class HomeView(View):
    template_name = 'app/home.html'

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        context = {
            'notes': notes
        }
        return render(request, self.template_name, context)

@method_decorator(otp_required, name='dispatch')
class AddNoteView(View):
    template_name = 'app/add_note.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = NoteForm(request.POST)
        if not form.is_valid():
            for error in form.errors:
                messages.error(request, form.errors[error])
            return render(request, self.template_name, {'form': form})
        content = form.cleaned_data['content']
        encrypted = form.cleaned_data['is_encrypted']
        password = form.cleaned_data['password']
        if encrypted and not password:
            messages.error(request, 'Password is required for encrypted notes')
            return render(request, self.template_name, {'form': form})
        if encrypted:
            encrypted_content, key = encrypt_content(content, password)
            Note.objects.create(user=request.user,
                                title=form.cleaned_data['title'],
                                content=encrypted_content,
                                is_public=form.cleaned_data['is_public'],
                                is_encrypted=True,
                                password=password,)
        else:
            Note.objects.create(user=request.user,
                                title=form.cleaned_data['title'],
                                content=content,
                                is_public=form.cleaned_data['is_public'],
                                is_encrypted=False,
                                password=None,)