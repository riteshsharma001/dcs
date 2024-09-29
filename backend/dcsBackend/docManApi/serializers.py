
# serializers.py
from rest_framework import serializers
from .models import LoginActivity

class LoginActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginActivity
        fields = '__all__'

        
##################

from rest_framework import serializers
from .models import DocumentSubmit

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSubmit
        fields = ['id', 'docname', 'document_Path', 'uploaded_at', 'user']
