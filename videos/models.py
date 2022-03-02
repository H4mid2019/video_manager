from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.dispatch import receiver



class Video(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to="video/")

    def __str__(self) -> str:
        return self.name


@receiver(models.signals.post_delete, sender=Video)
def auto_delete_video_on_delete(sender, instance, **kwargs):
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)
            

class User(AbstractUser):
    bio = models.TextField()

    def save(self, *args, **kwargs):
        if self.is_superuser:
            # this condition for createsuperuser via cli
            self.bio = "is_admin"

        return super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username