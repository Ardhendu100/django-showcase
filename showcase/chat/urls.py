from django.urls import path
from . import views 

urlpatterns = [
    path('chat/', views.chat_room, name='chat_default'), 
    path('chat/<str:room_name>/', views.chat_room, name='chat'),
]