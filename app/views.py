
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, VideoSerializer, VideoWithSubtitlesSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import subprocess
import json
import uuid
from .models import Videos, Subtitles
from django.core.files import File
# Create your views here.



class RegisterUser(APIView):

    def post(self, request):
        data = request.data
        if not data.get('email'):
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        data['username'] = data['email']
        ser_res = UserSerializer(data = data)
        if ser_res.is_valid():
            ser_res.save()
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(ser_res.errors, status=status.HTTP_400_BAD_REQUEST)


def get_subtitle_info(video_path):
    
    cmd = f'ffprobe -v error -select_streams s -show_entries stream=index:stream_tags=language -of json {video_path}'
    

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = json.loads(result.stdout)
    
    
    subtitle_streams = []
    for stream in output.get('streams', []):
        stream_info = {
            'index': stream['index'],
            'language': stream.get('tags', {}).get('language', 'unknown')
        }
        subtitle_streams.append(stream_info)
    
    return subtitle_streams




def extract_subtitles(video_path, output_dir, subtitle_streams):
    
    extracted_files = []
    
    for stream in subtitle_streams:
        file_name = f"{uuid.uuid4()}.srt"
        output_file = os.path.join(output_dir, file_name)
        command = f'ffmpeg -i  {video_path} -map 0:{stream["index"]} {output_file}'
        
        subprocess.run(command)

        if os.path.exists(output_file):
            extracted_files.append({
                'language': stream['language'],
                'file': output_file
            })
        
    return extracted_files

class UploadVideoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data =request.data
        
        
        data['user'] = request.user.id

        ser_res = VideoSerializer(data=data)
        if ser_res.is_valid():
            obj = ser_res.save()
            video_path = os.path.join(settings.MEDIA_ROOT, str(obj.video))


            subtitle_streams = get_subtitle_info(video_path)

            output_dir = os.path.join(settings.MEDIA_ROOT, 'subtitles')
            os.makedirs(output_dir, exist_ok=True)
            
            extracted_subtitles = extract_subtitles(video_path, output_dir, subtitle_streams)
            
            for subtitle in extracted_subtitles:
                
               
                    
                    Subtitles.objects.create(
                        video=obj,
                        language=subtitle['language'],
                        subtitle_file=subtitle['file']
                    )
            return Response(ser_res.data, status=status.HTTP_201_CREATED)
        return Response(ser_res.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUploadedVideosByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Videos.objects.filter(user = request.user.id)
        ser_res = VideoWithSubtitlesSerializer(data, many = True)
        return Response(ser_res.data, status=status.HTTP_200_OK)
    
class VideoDetailsView(APIView):

    permission_classes= [IsAuthenticated]
    def get(self,request, pk):
        data = get_object_or_404(Videos, pk= pk)
        ser_res = VideoWithSubtitlesSerializer(data)
        return Response(ser_res.data, status=status.HTTP_200_OK)
    

class VideoListView(APIView):

    def get(self,request):
        videos = Videos.objects.all()
        ser_res = VideoSerializer(videos, many= True)
        return Response(ser_res.data, status=status.HTTP_200_OK)