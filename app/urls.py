

from django.urls import path
from .views import RegisterUser,UploadVideoView, GetUploadedVideosByUserView, VideoDetailsView, VideoListView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView, TokenVerifyView)


urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register_user"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("upload-video/", UploadVideoView.as_view(), name="upload_video"),
    path("get-uploaded-videos-by-user/", GetUploadedVideosByUserView.as_view(), name= "get_uploaded_videos_by_user"),
    path("video-details/<uuid:pk>", VideoDetailsView.as_view(), name="video_details"),
    path("video-list/", VideoListView.as_view(), name="video_list"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
