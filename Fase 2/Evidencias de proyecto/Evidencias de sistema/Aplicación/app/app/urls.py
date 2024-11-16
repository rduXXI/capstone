from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", home, name="home"),
    path("", home, name="home_admin"),
    path("autenticacion/", include("autenticacion.urls")),
    path("cart/", include("cart.urls")),
    path("catalogo/", include("catalogo.urls")),
    path("canjeo/", include("canjeo.urls")),
    path("gestion/", include("gestion.urls")),
    path("orden_pedido/", include("orden_pedido.urls")),
    path("productos/", include("productos.urls")),
    path("puntos/", include("puntos.urls")),
    path("roles/", include("roles.urls")),
    path("sorteo/", include("sorteo.urls")),
    path("subasta/", include("subasta.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
