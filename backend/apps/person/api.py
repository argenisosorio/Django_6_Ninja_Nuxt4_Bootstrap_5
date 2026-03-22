from typing import List, Any
from django import forms
from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema, Schema
from .models import Person


# Inicializamos el Router de Ninja para agrupar estos endpoints
router = Router()

# --- DJANGO FORMS (Capa de Validación de Negocio) ---

class PersonForm(forms.ModelForm):
    """
    Utilizamos un ModelForm tradicional de Django para aprovechar las
    validaciones automáticas del modelo (Unique, MaxLength, etc.).
    Es el encargado de decidir si los datos son aptos para la base de datos.
    """
    class Meta:
        model = Person
        fields = ['name', 'email', 'age']

        error_messages = {
            'name': {
                'required': "API: El campo Nombre es obligatorio.",
                'invalid': "API: El campo Nombre solo debe contener letras y espacios.",
            },
            'email': {
                'required': "API: El campo Correo electrónico es obligatorio.",
                'invalid': "API: El campo Correo electrónico debe ser un correo válido.",
            },
            'age': {
                'required': "API: El campo Edad es obligatorio.",
                'invalid': "API: El campo Edad debe ser un número entero.",
                'min_value': "API: El campo Edad no puede ser negativo.",
                'max_value': "API: El campo Edad no puede ser mayor a 120 años.",
            },
        }

# --- SCHEMAS (Capa de Serialización / Pydantic) ---

class PersonSchema(ModelSchema):
    """
    Define cómo se verán los datos que SALEN hacia el cliente (Output).
    Ninja convierte automáticamente los objetos de Django a JSON.
    """
    class Meta:
        model = Person
        fields = ['id', 'name', 'email', 'age', 'created_at', 'updated_at']

class PersonCreateSchema(Schema):
    """
    Usamos Any = None para que Pydantic NO detenga la petición
    y permita que sea Django Form quien maneje los mensajes de error.

    Comentadas las validaciones de tipo para dejar pasar los datos.
    """
    #name: str
    #email: str
    #age: int
    name: Any = None
    email: Any = None
    age: Any = None

class ErrorSchema(Schema):
    """
    Esquema especial para documentar y estructurar las respuestas de error.
    Permite que el frontend sepa que recibirá un objeto con una llave 'errors'.
    """
    errors: dict

# --- ENDPOINTS (CRUD) ---

# 1. Listar personas (GET)
@router.get("/", response=List[PersonSchema])
def list_people(request):
    """Retorna un QuerySet que Ninja serializa como una lista de objetos."""
    return Person.objects.all()

# 2. Obtener una persona (GET por ID)
@router.get("/{person_id}", response=PersonSchema)
def get_person(request, person_id: int):
    """Busca un objeto o lanza un error 404 si no existe."""
    person = get_object_or_404(Person, id=person_id)
    return person

# 3. Crear una persona (POST)
@router.post("/", response={201: PersonSchema, 400: ErrorSchema})
def create_person(request, data: PersonCreateSchema):
    """
    Proceso de creación con validación doble:
    1. Ninja valida tipos (Pydantic).
    2. Django Form valida lógica de negocio (Email único, etc.).
    """
    # Convertimos el Schema de Ninja a un diccionario para el Form de Django
    form = PersonForm(data.dict())

    if form.is_valid():
        person = form.save()
        # Retornamos código 201 (Created) y el objeto creado
        return 201, person

    # Si el formulario falla, devolvemos 400 (Bad Request) y los errores.
    # get_json_data() estructura los errores para que sean fáciles de leer en JS.
    return 400, {"errors": form.errors.get_json_data()}

# 4. Actualizar una persona (PUT)
@router.put("/{person_id}", response={200: PersonSchema, 400: ErrorSchema})
def update_person(request, person_id: int, data: PersonCreateSchema):
    """
    Actualiza un registro existente vinculando la instancia al formulario.
    """
    person = get_object_or_404(Person, id=person_id)

    # El parámetro 'instance' es clave: permite a Django saber que es una edición
    # y evitar errores de validación de campos únicos contra sí mismo.
    form = PersonForm(data.dict(), instance=person)

    if form.is_valid():
        person = form.save()
        return 200, person

    return 400, {"errors": form.errors.get_json_data()}

# 5. Eliminar una persona (DELETE)
@router.delete("/{person_id}")
def delete_person(request, person_id: int):
    """Elimina el registro y confirma la operación."""
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return {"success": True, "message": f"Person {person_id} deleted successfully"}
