from django.contrib.auth.models import AbstractUser
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from Crypto.PublicKey import RSA

    
def initialize_private_key():
    return RSA.generate(2048).export_key('PEM')
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=False, default='a@a.com', blank=True)
    private_key = EncryptedCharField(max_length=3000, default=initialize_private_key)
    def __str__(self):
        return self.username