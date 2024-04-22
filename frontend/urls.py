from django.urls import path

from . import views

urlpatterns = [path("", views.home), path("up", views.up), path("stress", views.stress)]
