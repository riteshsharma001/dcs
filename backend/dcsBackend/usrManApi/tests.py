from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, UserProfile

class UserTests(TestCase):
    
    def setUp(self):
        # Create a test client
        self.client = APIClient()

        # Test user data
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123',
        }

        # Register the test user
        self.client.post(reverse('register'), self.user_data)

    def test_user_creation(self):
        # Test if the user is created
        user = CustomUser.objects.get(email='testuser@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_user_profile_creation(self):
        # Test if the user profile is automatically created
        user = CustomUser.objects.get(email='testuser@example.com')
        profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user.email, 'testuser@example.com')

    def test_user_login(self):
        # Test login functionality
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_invalid_login(self):
        # Test login with incorrect credentials
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        # Test logout functionality
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        })
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Call logout API
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from django.test import TestCase


