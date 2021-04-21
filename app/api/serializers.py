from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


from app.models import Passport


class PassportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passport
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_superuser']
        # fields = "__all__"



class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")