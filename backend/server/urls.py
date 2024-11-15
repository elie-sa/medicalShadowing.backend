from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('join-room', views.join_room, name='join_room'),
]
