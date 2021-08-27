from django.contrib import admin
from django.urls import path

from movie import views
from movie.views import listMovie

urlpatterns = [
    path('', listMovie),
]