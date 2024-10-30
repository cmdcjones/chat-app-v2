from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def register_user(request):
    data = request.data
    username = data['username']
    password = data['password']
    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create(
            username=username,
            password=make_password(password)
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    data = request.data
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return redirect('login_page')

def register(request):
    return render(request, 'chat/register.html')

def login_(request):
    return render(request, 'chat/login.html')

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    username = request.user.username
    return render(request, 'chat/room.html', {"room_name": room_name, "username": username})