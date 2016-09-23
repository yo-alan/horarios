# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from institucion import Institucion

class Usuario_directivo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1,
                                choices=[('F', 'F'), ('M', 'M')],
                                default='F')
    instituciones = models.ManyToManyField(Institucion)
