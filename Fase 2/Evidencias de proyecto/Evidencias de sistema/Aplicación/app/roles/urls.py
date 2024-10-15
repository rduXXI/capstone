from django.urls import path
from roles.views import asignar_puntos, crear_puntos

urlpatterns = [
    path('puntos/<int:id>/', asignar_puntos, name='asignar_puntos'),
    path('puntos/add', crear_puntos, name='crear_puntos'),
]