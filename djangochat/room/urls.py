from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('selenium/', views.selenium, name='selenium'),
    path('selenium/like/', views.like_video, name='like_video'),

    path('<slug:slug>/', views.room, name='room'),
    
]