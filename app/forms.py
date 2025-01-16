import django.forms as forms

class NoteForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=False)
    is_public = forms.BooleanField(required=False)
    shared_with = forms.CharField(max_length=100, help_text='Enter usernames separated by commas', label='Share with', required=False)
    is_encrypted = forms.BooleanField(required=False)
    password = forms.CharField(max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        is_encrypted = cleaned_data.get('is_encrypted')
        if is_encrypted and len(password) < 1:
            self.add_error('password', 'Encrypted message has to have a password')
        if not cleaned_data.get('is_public') and not cleaned_data.get('shared_with'):
            self.add_error('shared_with', 'You have to share the note with someone')
        return cleaned_data
    
class PasswordForm(forms.Form):
    password = forms.CharField(max_length=255, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        if not password:
            self.add_error('password', 'Password is required')
        return cleaned_data