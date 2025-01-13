import django.forms as forms

class NoteForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    is_public = forms.CheckboxInput()
    shared_with = forms.CharField(max_length=100)