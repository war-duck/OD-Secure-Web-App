from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from .helpers import derive_key
import base64
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
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
    signature = models.CharField(max_length=256, default='')

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
        return key == base64.b64decode(self.password)
    
    def sign(self):
        print('signing\n\n')
        message = self.content.encode()
        private_key = self.user.private_key.encode()
        signature = pkcs1_15.new(RSA.import_key(private_key)).sign(SHA256.new(message))
        self.signature = base64.b64encode(signature).decode()
        
    def save(self, *args, **kwargs):
        self.sign()
        super().save(*args, **kwargs)