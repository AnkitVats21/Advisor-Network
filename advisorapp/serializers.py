from rest_framework import serializers
from advisorapp.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name','email','password')
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        password    = validated_data.pop('password')
        user        = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        fields = ('email','password')
        extra_kwargs= {'password': {'write_only': True}}