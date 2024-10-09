from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        user = CustomUser.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
