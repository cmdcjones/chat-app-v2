from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('register/', views.register, name='register_page'),
    path('login/', views.login_, name='login_page'),
    path('logout/', views.logout_user, name='logout_user'),
    path('chat/', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room')
]
