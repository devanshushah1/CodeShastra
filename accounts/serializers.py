from rest_framework import serializers
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
    def validate(self, attrs):
        email = attrs.get('email', '')
        return attrs
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens']
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user=auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return super().validate(attrs)

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = ('__all__')

class ItemSerializer(serializers.ModelSerializer):
    keyword = serializers.StringRelatedField(many=True)
    class Meta:
        model = Item
        fields = ('__all__')

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claims
        fields = ('__all__')
