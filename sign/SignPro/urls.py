from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.homePage),
    path('index/', views.index, name='index'),
    path('tracking/', views.trackingTest, name='tracking'),
]
