from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
import random

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


def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    tag = '#' + ''.join([random.choice('ABCDEF0123456789') for _ in range(5)])
    username = request.GET.get('username', f'Anonymous{tag}')
    return render(request, 'chat/room.html', {"room_name": room_name, "username": username})