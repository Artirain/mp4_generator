from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.create_video, name='create_video'),
]
