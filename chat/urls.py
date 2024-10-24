from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('chat/', views.chat_view, name='chat')
]
