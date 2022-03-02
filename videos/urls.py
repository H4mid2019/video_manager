from django.urls import path
from .views import VideosVewSet, VideoVewSet, VideoUploadView, create_user, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Videos
    path('videos', VideosVewSet.as_view({'get': 'list'}), name='all_videos'),
    path('video/<int:video_id>', VideoVewSet.as_view()),
    path('video/upload', VideoUploadView.as_view(), name='upload'),
    # Users
    path('user/<str:username>', UserViewSet.as_view({
        'patch': 'update',
        'delete': 'destroy',
        'get': 'read'
    })),
    path("create_user", create_user, name="create_user"),
    # JWT
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]