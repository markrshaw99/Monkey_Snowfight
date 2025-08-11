from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', null=True, blank=True)
    default_avatar = models.CharField(max_length=50, null=True, blank=True)  # Store default avatar selection
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True) 
    
    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        if self.displayname:
            return self.displayname
        return self.user.username 
    
    @property
    def avatar(self):
        # Priority: Custom uploaded image > Default avatar selection > Fallback avatar
        if self.image:
            return self.image.url
        elif self.default_avatar:
            return f'{settings.STATIC_URL}images/defaultAvatars/{self.default_avatar}'
        return f'{settings.STATIC_URL}images/avatar.png'
