from rest_framework import serializers
from .models import Video, User


class VideoDetailsSerializer(serializers.ModelSerializer):
    """serializes data from the model 

    Args:
        serializers (django db model): it gets the django db model named Video
    """

    class Meta:
        model = Video
        fields = '__all__'



class VideoListSerializer(serializers.ModelSerializer):
    """serializes data from the model 

    Args:
        serializers (django db model): it gets the django db model named Video
    """

    class Meta:
        model = Video
        fields = ('id', 'name')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'bio',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            bio=validated_data["bio"]
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
