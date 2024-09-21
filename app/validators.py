from rest_framework import serializers
import re
import os

def validate_email(email):
    
    email_regex =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(email_regex, email):
        raise serializers.ValidationError("Email is not valid.")
    return email

def validate_password(password):
    
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    if not re.fullmatch(password_regex, password):
        raise serializers.ValidationError("The password should have atleast length of 8, one uppcase , one lowercase , one number and one special character.")
    return password

def validate_video(video):
    
    valid_mime_types = ['video/mp4', 'video/x-matroska', 'video/x-msvideo', 'video/quicktime']
    valid_file_extensions = ['.mp4', '.mkv', '.avi', '.mov']
   

    # Check file type (MIME)
    if video.content_type not in valid_mime_types:
        raise serializers.ValidationError(f"Unsupported file type. Allowed types are: {', '.join(valid_mime_types)}.")

    # Check file extension
    ext = os.path.splitext(video.name)[1]
    
    if ext.lower() not in valid_file_extensions:
        raise serializers.ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(valid_file_extensions)}.")

  