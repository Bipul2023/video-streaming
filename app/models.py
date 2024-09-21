from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Videos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.CharField(max_length=300)
    video = models.FileField(upload_to="videos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Subtitles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE , related_name='subtitle')
    language = models.CharField(max_length=250)
    subtitle_file = models.FileField(upload_to='subtitles/')
    
