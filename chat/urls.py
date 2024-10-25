from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register_user, name='register'),
    path('chat/', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='lobby')
]
