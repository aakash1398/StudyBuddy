from django.urls import path,include
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('login/',login_user, name='login'),
    path('logout/',logout_user, name='logout'),
    path('register/',register_user, name='register'),


    path('room/<int:pk>/',room, name='room'),
    path('create-room/', create_room, name='create-room'),
    path('update-room/<int:pk>/', update_room, name='update-room'),
    path('delete-room/<int:pk>/', delete_room, name='delete-room'),

    path('delete-room-message/<int:pk>/', delete_room_message, name='delete-room-message')
]
