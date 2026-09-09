
from django.db import models

from django.conf import settings
from core.models import TimeStampMixin
# Create your models here.


class Post(TimeStampMixin):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE, 
            related_name='posts')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    text = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.text[0:15]

     
