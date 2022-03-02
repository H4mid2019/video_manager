from django.contrib import admin
from .models import User, Video

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','name')
