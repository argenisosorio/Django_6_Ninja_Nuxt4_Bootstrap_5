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

# Diccionario global de traducciones para Pydantic v2
DICCIONARIO_ERRORES = {
    "missing": "Este campo es obligatorio.",
    "string_too_short": "El campo no puede estar vacío.",
    "value_error": "El valor ingresado no es válido.",
    # Errores de Email
    "value_error.email": "El correo electrónico no es válido.",
    "email_parsing": "El formato del correo electrónico es incorrecto (debe incluir @).",
    # Errores de Números (Edad)
    "int_parsing": "Debes ingresar un número entero válido.",
    "int_type": "Este campo debe ser un número.",
}

@api.exception_handler(ValidationError)
def custom_validation_errors(request, exc):
    errors = {}
    for error in exc.errors:
        field_name = error["loc"][-1]
        error_type = error["type"]

        # 1. Buscamos si tenemos una traducción exacta para ese tipo de error
        # 2. Si no existe, usamos el mensaje por defecto que trae Pydantic
        mensaje_espanol = DICCIONARIO_ERRORES.get(error_type, error["msg"])

        errors[field_name] = mensaje_espanol

    return api.create_response(
        request,
        {"errors": errors},
        status=422
    )
