# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from calendario.models import Persona
from institucion import Institucion

class Usuario(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1,
                                choices=[('F', 'F'), ('M', 'M')],
                                default='F')
    instituciones = models.ManyToManyField(Institucion)
