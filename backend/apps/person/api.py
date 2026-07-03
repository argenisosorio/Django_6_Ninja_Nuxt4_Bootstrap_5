from typing import List, Any
from django import forms
from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema, Schema
from pydantic import field_validator, EmailStr
from .models import Person


# Inicializamos el Router de Ninja para agrupar estos endpoints
router = Router()

# --- SCHEMAS (Capa de Serialización / Pydantic) ---


class PersonSchema(ModelSchema):
    """
    Define cómo se verán los datos que SALEN hacia el cliente (Output).
    Ninja convierte automáticamente los objetos de Django a JSON.
    """
    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'email',
            'age',
            'created_at',
            'updated_at'
        ]


class PersonCreateSchema(Schema):
    """
    Usamos Any = None para que Pydantic NO detenga la petición
    y permita que sea Django Form quien maneje los mensajes de error.

    Comentadas las validaciones de tipo para dejar pasar los datos.
    """
    name: str
    email: EmailStr
    age: int

# --- ENDPOINTS (CRUD) ---

# Listar personas (GET)
@router.get("/", response=List[PersonSchema])
def list_people(request):
    """
    Retorna un QuerySet que Ninja serializa como una lista de objetos.
    """
    return Person.objects.all()


# Crear una persona (POST)
@router.post("/", response={201: PersonSchema})
def create_person(request, data: PersonCreateSchema):
    # Si llega aquí, los datos ya son 100% válidos y limpios
    person = Person.objects.create(**data.dict())
    return 201, person
