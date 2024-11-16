from django.urls import path
from . import views

urlpatterns = [
    path("catalogo/", views.lista_catalogo, name="modo_lista"),
    path("catalogo-modo-grilla/", views.view_catalogo, name="catalogo"),
    
]
