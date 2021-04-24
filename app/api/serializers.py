from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings

from app.models import Passport
from app.cryptography import AESCipher


class PassportSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # firstname = serializers.CharField()
    # lastname = serializers.CharField()
    # middlename = serializers.CharField()
    # phone = serializers.IntegerField()
    # address = serializers.CharField()
    # tin = serializers.CharField()
    class Meta:
        model = Passport
        fields = [
            "id",
            "firstname",
            "lastname",
            "middlename",
            "phone",
            "address",
            "tin",
            "sensitive_data"
        ]

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     cipher = AESCipher(settings.ENCRYPT_SECRET_KEY)
    #     print(validated_data)
    #     print(cipher.decrypt(validated_data["tin"]))
    #     validated_data["tin"] = cipher.decrypt(validated_data["tin"]).encode("ascii")
    #     return Passport.objects.create(**validated_data)

    # def create(self, validated_data):
    #     cipher = AESCipher(settings.ENCRYPT_SECRET_KEY)
    #     user = super(PassportSerializer, self).create(validated_data)
    #     # print('>>>>>>>>>', validated_data)
    #     user.tin = cipher.encrypt(str(123132123))
    #     user.save()
    #     return user

    # def to_representation(self, instance):
    #     cipher = AESCipher(settings.ENCRYPT_SECRET_KEY)
    #     ret = super().to_representation(instance)
    #     ret['firstname'] = ret['firstname'].lower()
    #     # print(cipher.decrypt(ret['tin']))
    #     ret['tin'] = cipher.decrypt(ret['tin'])
    #     return ret

    # def to_representation(self, data):
    #     cipher = AESCipher(settings.ENCRYPT_SECRET_KEY)
    #     print(data.tin[2][-1])
    #     # print(cipher.decrypt(data.tin))
    #     return {
    #         'id': data.id,
    #         'firstname': data.firstname.lower(),
    #         "lastname": data.lastname,
    #         "middlename": data.middlename,
    #         "phone": data.phone,
    #         "address": data.address,
    #         # 'tin': cipher.decrypt(data.tin[2,-1])
    #     }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "is_superuser",
        ]


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")