from rest_framework import serializers
from advisorapp.models import User
from advisorapp import models


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

class AdvisorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Advisor
        fields = '__all__'


class AdvisorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Advisor
        fields = '__all__'


class BookedCallSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BookedCall
        fields = ('booking_time',)


class BookedCallListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BookedCall
        fields = '__all__'

    
    def to_representation(self, instance):
        ret     = super().to_representation(instance)
        advisorid      = ret['advisor']
        advisor = models.Advisor.objects.get(id=advisorid)
        serializer  = AdvisorSerializer(advisor, context={'request': self.context.get('request')})
        returnlist ={
            'advisorName':serializer.data.get('advisor_name'),
            'advisorPhoto':serializer.data.get('advisor_photo'),
            'advisorId':serializer.data.get('id'),
            'bookingTime': ret['booking_time'],
            'bookingId':ret['id']
        }
        return returnlist