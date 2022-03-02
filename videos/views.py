from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Video, User
from .serializers import VideoListSerializer,VideoDetailsSerializer, UserSerializer
import logging

logger = logging.getLogger(__name__)



class VideoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = VideoDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)




class VideosVewSet(viewsets.ViewSet):
    
    def list(self, request):
        """this method retruns the all products
        """
        videos = Video.objects.all()
        serializer = VideoListSerializer(videos, many=True)
        return Response(serializer.data)



class VideoVewSet(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, video_id=None):
        video = get_object_or_404(Video, id=video_id)
        serializer = VideoDetailsSerializer(video)
        return Response(serializer.data)


    def patch(self, request, video_id=None):
        video = get_object_or_404(Video, id=video_id)
        serializer = VideoDetailsSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    """this view function creates a user so then the user can obtain a token
    """
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid(raise_exception=True):
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):

    def update(self, request, username=None):
        with transaction.atomic():
            user = User.objects.select_for_update().get(username=username)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, username=None):
        with transaction.atomic():
            user = User.objects.select_for_update().get(username=username)
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def read(self, request, username=None):
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
