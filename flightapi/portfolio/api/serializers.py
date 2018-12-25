from account.models import User
from rest_framework import serializers


class FastPaceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class CreateFastPaceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class FastPaceLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class JSONWebTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=225)

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'profile_photo')
