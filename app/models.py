from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from .helpers import decrypt_content, derive_key
import base64
User = get_user_model()
    
class Note(models.Model):
    title = models.CharField(max_length=100, blank=False, default='Untitled')
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(CustomUser, related_name='shared_with', blank=True)
    is_encrypted = models.BooleanField(default=False)
    password = models.CharField(max_length=512, blank=True, null=True)
    def __str__(self):
        return self.title
    
    def is_accessible(self, user):
        if self.is_public:
            return True
        elif self.shared_with.contains(user):
            return True
        elif self.user == user:
            return True
        else:
            return False
        
    def verify_password(self, password):
        key = derive_key(password, base64.b64decode(self.content.split('$')[1]))
        print(key)
        print(base64.b64decode(self.password))
        return key == base64.b64decode(self.password)