from django.contrib import admin
from django.urls import include, path
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('autenticacion/', include('autenticacion.urls')),
    path('canjeo/', include('canjeo.urls')),
    path('gestion/', include('gestion.urls')),
    path('roles/', include('roles.urls')),
    path('productos/', include('productos.urls')),
    path('puntos/', include('puntos.urls')),
    path('', home, name='home'),

]
