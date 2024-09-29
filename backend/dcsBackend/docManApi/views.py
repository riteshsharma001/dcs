from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import generics
from .models import LoginActivity
from .serializers import LoginActivitySerializer

class LoginActivityList(generics.ListAPIView):
    queryset = LoginActivity.objects.all()
    serializer_class = LoginActivitySerializer

################

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DocumentSubmit
from .serializers import DocumentSerializer

class DocumentSubmitView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
