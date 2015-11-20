# -*- coding: utf-8 -*-
from django.db import models

from espacio import Espacio

class DiaHabil(models.Model):
    """
    DEFINICION.
    
    @Atributos:
    .espacio - Espacio.
    .dia - Integer.
    """
    
    espacio = models.ForeignKey(Espacio)
    dia = models.IntegerField(default=0, null=False)
