# -*- coding: utf-8 -*-
from django.db import models

from calendario import Calendario
from coordinador import Coordinador

class Horario(models.Model):
    
    hora_desde = models.TimeField('desde', null=False)
    hora_hasta = models.TimeField('hasta', null=False)
    dia_semana = models.IntegerField(default=0, null=False)
    penalizado = models.IntegerField(default=0)
    movible = models.BooleanField(default=True)
    calendario = models.ForeignKey(Calendario)
    coordinador = models.ForeignKey(Coordinador, null=True)
    
    def __str__(self, ):
        return str(self.coordinador.especialidad)
    
    def __eq__(self, o):
        return self.hora_desde == o.hora_desde and\
                self.dia_semana == o.dia_semana
    
    def __ne__(self, o):
        return self.dia_semana != o.dia_semana and\
                self.hora_desde != o.hora_desde
    
    def __lt__(self, o):
        if self.dia_semana == o.dia_semana:
            return self.hora_desde < o.hora_desde
        
        return self.dia_semana < o.dia_semana
    
    def __le__(self, o):
        if self.dia_semana == o.dia_semana:
            return self.hora_desde <= o.hora_desde
        
        return self.dia_semana <= o.dia_semana
    
    def __gt__(self, o):
        if self.dia_semana == o.dia_semana:
            return self.hora_desde > o.hora_desde
        
        return self.dia_semana > o.dia_semana
    
    def __ge__(self, o):
        if self.dia_semana == o.dia_semana:
            return self.hora_desde >= o.hora_desde
        
        return self.dia_semana >= o.dia_semana
