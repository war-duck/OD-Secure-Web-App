from django_otp.decorators import otp_required
from .models import Note
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator

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
    
    