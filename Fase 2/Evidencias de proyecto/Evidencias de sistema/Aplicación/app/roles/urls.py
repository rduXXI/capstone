from django.urls import path
from . import views

urlpatterns = [
    path("puntos/add/", views.add_puntos, name="add_puntos"),
    path("puntos/change/<int:id>/", views.change_puntos, name="change_puntos"),
]
