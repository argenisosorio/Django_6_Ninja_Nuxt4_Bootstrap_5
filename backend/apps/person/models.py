from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

class Person(models.Model):
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Nombre"
    )

    # EmailField ya valida el formato de correo por defecto en Django
    email = models.CharField(
        null=True,
        blank=True,
        verbose_name="Correo Electrónico"
    )

    # Validamos que sea entre 0 y 120 años
    age = models.CharField(
        null=True,
        blank=True,
        verbose_name="Edad"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
