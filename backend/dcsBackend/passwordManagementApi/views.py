from django.shortcuts import render
from rest_framework.views import APIView
from usrManApi.models import CustomUser
from .models import UserReset
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your views here.

class ChangePasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        oldpassword = request.data.get('old_password')
        newpassword = request.data.get('new_password')
        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(oldpassword):
            user.set_password(newpassword)
            user.save()
            return Response({'status':'Password changes success'}, status=status.HTTP_200_OK)
        return Response({'error': "Invalid credentials "}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        user = CustomUser.objects.filter(email = email).first()
        if user in None:
            return Response({'email': 'user with given email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        token = PasswordResetTokenGenerator().make_token(user)
        UserReset.objects.create(email=user, reset_token=token)
        resetLink = f"http://frontend/reset-password/{token}"
        send_mail('Reset your password', resetLink, 'demo@gmail.com', [user.email])
        return Response({'success': 'Password reset link has been sent to your email.'}, status = status.HTTP_200_OK)

class ResetPasswordConfirmView(APIView):
    def post(self, request):
        token = request.data['token']
        password = request.data['password']

        tokenEntry = UserReset.objects.filter(reset_token=token).first()
        if tokenEntry is None:
            return Response({'error':"Invalid token"}, status = status.HTTP_400_BAD_REQUEST)

        user = tokenEntry.email
        user.set_password(password)
        user.save()
        tokenEntry.delete()
        return Response({'success': 'Password reset success'}, status=status.HTTP_200_OK)