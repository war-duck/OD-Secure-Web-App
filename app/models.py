from django.db import models
from accounts.models import CustomUser
    
class Note(models.Model):
    title = models.CharField(max_length=100, blank=False, default='Untitled')
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(CustomUser, related_name='shared_with', blank=True)
    is_encrypted = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.title
    
    def is_accessible(self, user):
        if self.is_public:
            return True
        elif user == self.user:
            return True
        elif user in self.shared_with.all():
            return True
        else:
            return False