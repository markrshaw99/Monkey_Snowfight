from django.db import models
from django.contrib.auth.models import User
import shortuuid
import os
from PIL import Image
from cloudinary.models import CloudinaryField


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, blank=True, null=True)
    admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name
    

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    file = CloudinaryField('file', resource_type='auto', blank=True, null=True)
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        if self.original_filename:
            return self.original_filename
        elif self.file:
            return os.path.basename(self.file.url)
        else:
            return None

    def __str__(self):
        if self.body:
            return f'{self.author.username} : {self.body}'
        elif self.file:
            return f'{self.author.username} sent a file \"{self.filename}\"'
        return f'{self.author.username} (empty message)'

    class Meta:
        ordering = ['-created']

    @property
    def is_image(self):
        if self.file and self.file.url:
            ext = os.path.splitext(self.file.url)[1].lower()
            return ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
        return False
