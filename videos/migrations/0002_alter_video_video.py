# Generated by Django 3.2 on 2022-03-14 14:03

from django.db import migrations, models
import videos.models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='video/', validators=[videos.models.validate_video]),
        ),
    ]
