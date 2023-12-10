from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.urls import reverse
from .resources import *


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=ROLES, default=tanks)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    time_in = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
