from django.core.files.base import File
import os
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import User, Video



class VideoTest(TestCase):
    sample_password = "foo+secretpass"
    sample_username = 'test'
    sample_email = 'test@test.com'
    api_client = APIClient()
    sample_video_id = 0
    sample_video_name = 'test'
    access_JWT_token = ''


    def setUp(self):
        user = User(email=self.sample_email, username=self.sample_username, bio="biography")
        user.set_password(self.sample_password)
        user.save()
        response = self.api_client.post(reverse('token_obtain_pair'),{'username': self.sample_username, 'password':self.sample_password},format="json")
        self.access_JWT_token = response.data.get('access')
        # creating sample video
        with open('test.mp4', 'rb') as file:
            sample_video = Video.objects.create(name='test', video=File(file))
            self.sample_video_id = sample_video.id

    def test_setup_approval(self):
        """ This method approve the setup worked perfectly, which means the model and setup logic are working"""
        users_count = User.objects.count()
        self.assertEqual(1, users_count)
        video_counts = Video.objects.count()
        self.assertEqual(video_counts, 1)
        self.assertIsNotNone(self.access_JWT_token)
    
    def test_get_videos_without_JWT(self):
        """ an example for testing which without JWT doesn't work. It's a applicable all other endpoints."""
        response = self.api_client.get(reverse('all_videos'))
        self.assertEqual(response.status_code, 401)
        self.assertIsNotNone(response.data.get("detail"))
        
    def test_get_videos(self):
        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_JWT_token)
        response = self.api_client.get(reverse('all_videos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get("id"), self.sample_video_id)

  
    def test_upload_video(self):
        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_JWT_token)
        with open('test.mp4', 'rb') as file:
            response = self.api_client.post(reverse('upload'), {"name": "test_upload", "video": File(file)} ,format='multipart')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data.get('name'), 'test_upload')
            self.assertIsNotNone(response.data.get('video'))
    
    def test_get_video(self):
        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_JWT_token)
        response = self.api_client.get(f'/api/video/{self.sample_video_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), self.sample_video_id)
    
    def test_update_video_name(self):
        new_name= "changed"
        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_JWT_token)
        response = self.api_client.patch(f'/api/video/{self.sample_video_id}', data={"name": new_name}, format='multipart')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data.get("name"), new_name)

    def test_update_video(self):
        new_name= "new_name"
        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + self.access_JWT_token)
        with open('test.mp4', 'rb') as file:
            response = self.api_client.patch(f'/api/video/{self.sample_video_id}', data={"name": new_name, "video": File(file)}, format='multipart')
            self.assertEqual(response.status_code, 202)
            self.assertEqual(response.data.get("name"), new_name)