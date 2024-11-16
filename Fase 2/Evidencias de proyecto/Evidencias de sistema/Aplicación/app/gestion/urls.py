from django.urls import path
from . import views

urlpatterns = [
    path("movimientos/add/", views.add_movimiento, name="add_movimiento"),
]
