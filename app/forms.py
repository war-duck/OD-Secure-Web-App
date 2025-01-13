import django.forms as forms

class NoteForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=False)
    is_public = forms.CheckboxInput()
    shared_with = forms.CharField(max_length=100, help_text='Enter usernames separated by commas', required=False)