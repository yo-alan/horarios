# -*- coding: utf-8 -*-
from django.db import models

from espacio import Espacio

class Hora(models.Model):
    
    hora_desde = models.TimeField('desde', null=False)
    hora_hasta = models.TimeField('hasta', null=False)
    espacio = models.ForeignKey(Espacio)
    
    def __str__(self, ):
        return str(self.hora_desde)
