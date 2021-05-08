from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
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

    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data.get('id')
            user = User.objects.get(id=user_id)
            token = get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
