from django_otp.decorators import otp_required
from .models import Note
from django.template import loader
from django.http import HttpResponse

@otp_required
def home(request):
    notes = Note.objects.filter(user=request.user)
    template = loader.get_template('app/home.html')
    context = {
        'notes': notes
    }
    return HttpResponse(template.render(context, request))