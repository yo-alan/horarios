# -*- coding: utf-8 -*-
from django.db import models
from calendario import Calendario
from profesional import Profesional

class Restriccion(models.Model):
    
    hora_desde = models.TimeField('desde', null=False, blank=False)
    hora_hasta = models.TimeField('hasta', null=False, blank=False)
    dia_semana = models.IntegerField(default=0, null=False, blank=False)
    profesional = models.ForeignKey(Profesional)
    calendario = models.ForeignKey(Calendario, null=True)
    estado = models.CharField(max_length=3,
                                choices=[('ON', 'ON'), ('OFF', 'OFF')],
                                default='ON')
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30, default='admin')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("hora_desde", "hora_hasta", "dia_semana", "calendario")
    
    def sethora_desde(self, hora_desde):
        
        if hora_desde == "":
            raise Exception("La hora desde no puede ser vacía.")
        
        self.hora_desde = hora_desde
    
    def sethora_hasta(self, hora_hasta):
        
        if hora_hasta == "":
            raise Exception("La hora hasta no puede ser vacía.")
        
        self.hora_hasta = hora_hasta
    
    def setdia_semana(self, dia_semana):
        
        if dia_semana == "" or dia_semana < 0 or dia_semana > 7:
            raise Exception("El día de la semana no es válido.")
        
        self.dia_semana = dia_semana
