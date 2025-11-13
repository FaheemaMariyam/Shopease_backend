from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['id', 'name', 'email', 'phone', 'address', 'pin', 'role', 'password1', 'password2']
    def validate(self, data):
        if data['password1']!=data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        #Run Django's built-in password validation
        try:
            validate_password(data['password1'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.pop('password1'))#for hashing the password
        validated_data.pop('password2')
        email = validated_data.get('email')
        validated_data['username'] = email
        user = User.objects.create(**validated_data)
        return user  
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'name', 'email', 'phone', 'address', 'pin', 'role']