from rest_framework import serializers
from .models import CustomUser, UserProfile

## Serializer for the UserProfile model

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth']


 # Serializer for the CustomUser model       

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        # Pop the profile data from validated data
        profile_data = validated_data.pop('profile')
        
        # Create the user object
        user = CustomUser.objects.create(**validated_data)
        
        # Create the user profile linked to the user
        UserProfile.objects.create(user=user, **profile_data)
        
        return user

    def update(self, instance, validated_data):
        # Update the user profile along with user
        profile_data = validated_data.pop('profile', None)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.address = profile_data.get('address', profile.address)
            profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
            profile.save()

        return instance
