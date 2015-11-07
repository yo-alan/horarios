# -*- coding: utf-8 -*-
from django.db import models

class Penalidad(models.Model):
    """
    Objeto que contiene el punto de penalidad de cada restricción.
    
    @Atributos:
    .nombre: Nombre de la restricción.
    .puntos: Puntos de penalización de la restricción.
    """
    
    nombre = models.CharField(max_length=100, null=False, blank=False)
    puntos = models.IntegerField(default=0, null=False, blank=False)
    
    @classmethod
    def create(cls, nombre=''):
        
        if nombre != '':
            return Penalidad.objects.filter(nombre=nombre)[0]
        
        return Penalidad()
    
