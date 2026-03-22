from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'age']

        # Personalización de todos los mensajes de error capturados por el form
        error_messages = {
            'name': {
                'required': "FORM: El campo Nombre es obligatorio.",
                'invalid': "FORM: El campo Nombre solo debe contener letras y espacios.",
            },
            'email': {
                'required': "FORM: El campo Correo electrónico es obligatorio.",
                'invalid': "FORM: El campo Correo electrónico debe ser un correo válido.",
            },
            'age': {
                'required': "FORM: El campo Edad es obligatorio.",
                'invalid': "FORM: El campo Edad debe ser un número entero.",
                'min_value': "FORM: El campo Edad no puede ser negativo.",
                'max_value': "FORM: El campo Edad no puede ser mayor a 120 años.",
            },
        }

        # Agregamos clases de Bootstrap
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '120'}),
        }
