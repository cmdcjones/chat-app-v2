from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render

@api_view(['POST'])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create(
            username=data['username'],
            password=make_password(data['password'])
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    except:
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)


def chat_view(request):
    return render(request, 'index.html')