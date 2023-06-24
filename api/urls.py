from django.urls import path

from . import views


urlpatterns = [
    path("files", views.files),
    path("delete", views.delete),
    path("move", views.move),
    path("rename", views.rename),
]
