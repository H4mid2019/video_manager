from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import magic
from io import BytesIO
from django.core.exceptions import ValidationError
import logging


logger = logging.getLogger(__name__)

def validate_video(value):
    file = BytesIO(value.read())
    file_size = file.getbuffer().nbytes
    if file_size <= 150:
        raise ValidationError(_('Video size can\'t be zero.'))
    try:
        video_mimes = ['video/mp4', 'video/ogg', 'video/x-msvideo', 'video/x-ms-wmv']
        file_mime = magic.from_buffer(file.read(2048), mime=True)
        if not file_mime in video_mimes:
            raise ValidationError(_('You can only upload video files.'))
    except Exception as e:
        print(str(e))
        logger.error(str(e))
        raise ValidationError(_(str(e)))


class Video(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to="video/", validators=[validate_video], help_text='Only video files are allowed.')

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