from typing import List, Any
from django import forms
from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema, Schema
# Importamos Field y constr para aplicar restricciones y mensajes personalizados
from pydantic import field_validator, EmailStr, Field, constr
from .models import Person
from ninja.errors import HttpError
import json


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
    name: str
    email: str
    age: str

# --- FORMULARIO DE DJANGO ---
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'age']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # 1. Si ni siquiera llegó un nombre o es una cadena vacía
        if not name or not name.strip():
            raise forms.ValidationError("El nombre es requerido.")

        # 2. Si llegó pero es muy corto
        if len(name.strip()) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")

        # 3. Si todo está perfecto, retornamos el string limpio
        return name.strip()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # 1. Si ni siquiera llegó un email o es una cadena vacía
        if not email or not email.strip():
            raise forms.ValidationError("El email es requerido.")

        # 2. Si llegó pero es muy corto
        if len(email.strip()) < 10:
            raise forms.ValidationError("El email debe tener al menos 10 caracteres.")

        # 3. Si todo está perfecto, retornamos el string limpio
        return email.strip()


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
    # Creamos un diccionario con los datos que nos envía la resta del cliente y
    # lo pasamos al formulario de Django.
    form = PersonForm(data.dict())

    # Si el formulario es válido, guardamos la persona y retornamos un 201 con
    # el objeto creado.
    if form.is_valid():
        person = form.save()
        return 201, person
    # Si el formulario NO es válido, retornamos un 400 con los errores de
    # validación.
    else:
        # form.errors.get_json_data() nos da un diccionario nativo de Python:
        # {'name': [{'message': 'El nombre debe tener...', 'code': 'min_length'}]}
        raw_errors = form.errors.get_json_data()

        # Lo "aplanamos" para dejarlo en: {'name': 'El nombre debe tener...'}
        clean_errors = {
            field: messages[0]['message'] 
            for field, messages in raw_errors.items()
        }

        # Retornamos un 400 mandando el diccionario estructurado dentro de una llave 'errors'
        # Usamos json.dumps para pasarlo como texto válido al HttpError
        raise HttpError(400, json.dumps({"errors": clean_errors}))
