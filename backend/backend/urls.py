from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI
from ninja.errors import ValidationError
# Importamos el router de la app person
from apps.person.api import router as person_router

# 1. Instanciamos la API
api = NinjaAPI(title="Mi Proyecto CRUD API")

# 2. Añadimos los routers de cada app (puedes añadir el de products luego)
api.add_router("/person/", person_router)

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Tus rutas de templates/vistas tradicionales
    path('', include('apps.person.urls')),

    # 3. La ruta para TODA la API y su documentación
    path("api/", api.urls),
]

@api.exception_handler(ValidationError)
def custom_validation_errors(request, exc):
    """
    Transforma los errores de Pydantic en un JSON plano: {"campo": "error"}
    """
    errors = {}
    for error in exc.errors:
        # error['loc'] contiene la ubicación del campo (ej. ('body', 'email'))
        # Tomamos el último elemento que es el nombre del campo
        field_name = error["loc"][-1]
        errors[field_name] = error["msg"]

    return api.create_response(
        request,
        {"errors": errors},
        status=422
    )