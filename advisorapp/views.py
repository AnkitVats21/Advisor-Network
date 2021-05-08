from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from advisorapp import models, serializers
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView


def get_tokens_for_user(user):
    """
    function to get refresh and access token
    """

    refresh = RefreshToken.for_user(user)
    return {
        'id': user.id,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CreateUserAccount(APIView):
    """
    API view to create user account
    """

    serializer_class = serializers.UserSerializer
    
    def post(self, request):
        serializer = serializers.UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data.get('id')
            user = User.objects.get(id=user_id)
            token = get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    User Login View
    Returns jwt tokens and user id on valid request data.
    """

    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = User.objects.filter(email=email)
            if user:
                user = user[0]
                if user.check_password(password):
                    token = get_tokens_for_user(user)
                    return Response(token, status=status.HTTP_200_OK)
                return Response({'detail':'wrong password'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'detail':'acoount with given email address does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdvisorView(APIView):
    """
    Add advisor
    """

    serializer_class = serializers.AdvisorSerializer

    def post(self, request):
        serializer = serializers.AdvisorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvisorListView(APIView):
    """
    List of advisors
    """
    
    serializer_class = serializers.AdvisorSerializer

    def get(self, request, userid):

        try:
            user = User.objects.get(id=userid)
        except:
            return Response({'detail':'invalid user id.'}, status=status.HTTP_400_BAD_REQUEST)
        advisor = models.Advisor.objects.all()
        serializer = serializers.AdvisorSerializer(advisor, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookedCallView(APIView):
    """
    as per the recommendation of assignment
    user id and advisor id is taken from the url route
    """
    
    serializer_class = serializers.BookedCallSerializer

    def post(self,request,userid,advisorid):
        data = request.data.copy()
        data['user']=userid
        data['advisor']=advisorid
        serializer = serializers.BookedCallSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Bookings(APIView):
    """
    List of bookings by a user
    """
    
    serializer_class = serializers.BookedCallListSerializer

    def get(self, request, userid):
        try:
            user = User.objects.get(id=userid)
        except:
            return Response({'detail':'invalid user id.'}, status=status.HTTP_400_BAD_REQUEST)
        bookings = models.BookedCall.objects.filter(user=userid)
        serializer = serializers.BookedCallListSerializer(bookings, many=True, context={'request': request})    
        return Response(serializer.data, status=status.HTTP_200_OK)
        