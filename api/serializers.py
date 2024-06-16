from rest_framework import serializers
from .models import Friends
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ['id', 'request_to', 'status']

    def create(self, validated_data):
        request_from = self.context['request'].user
        friend_request, created = Friends.objects.get_or_create(
            request_to=validated_data['request_to'],
            request_from=request_from,
            defaults={'status': False}
        )
        if not created:
            raise serializers.ValidationError("Friend request already exists.")
        return friend_request

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Credentials")
