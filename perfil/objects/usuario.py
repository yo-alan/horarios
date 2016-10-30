# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from persona import Persona
from institucion import Institucion

class Usuario(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30,
                                            default='admin')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    instituciones = models.ManyToManyField(Institucion)
