from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from .validators import validate_email, validate_password, validate_video
import os
# import tempfile
from django.conf import settings
import subprocess

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators = [validate_email])
    password = serializers.CharField(validators = [validate_password])
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', "")
        )
        return user
    


class VideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(validators = [validate_video])
    
    class Meta:
        model = Videos
        fields = "__all__"

    def create(self, validated_data):
        video = validated_data['video']
        
       
        original_video_path = os.path.join(settings.MEDIA_ROOT, 'temp_videos', video.name)
        
        
        with open(original_video_path, 'wb+') as f:
            for chunk in video.chunks():
                f.write(chunk)

        
        ext = os.path.splitext(video.name)[1]
        compressed_video_path = self.compress_video(original_video_path,ext)

        validated_data['video'] = compressed_video_path

        os.remove(original_video_path)

        return super().create(validated_data)

    
    def compress_video(self, input_file_path, ext):

        output_file_name = f"{uuid.uuid4()}{ext}"
        output_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', output_file_name)
        
       
        ffmpeg_command = 'ffmpeg -i ' + input_file_path + ' -vcodec libx264 -crf 28 -preset fast '+ output_file_path 
        

        try:
           
            subprocess.run(ffmpeg_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise serializers.ValidationError(f"Video compression failed: {e}")
        
        return output_file_path


class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitles
        fields = "__all__"

class VideoWithSubtitlesSerializer(serializers.ModelSerializer):
    subtitle = SubtitleSerializer(many = True, read_only = True)
    class Meta:
        model = Videos
        fields = ['id', 'user', 'title', 'video', 'uploaded_at', 'subtitle']
