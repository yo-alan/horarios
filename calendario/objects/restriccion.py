# -*- coding: utf-8 -*-
from django.db import models

class Restriccion(models.Model):
    
    hora_desde = models.TimeField('desde', null=False, blank=False)
    hora_hasta = models.TimeField('hasta', null=False, blank=False)
    dia_semana = models.IntegerField(default=0, null=False, blank=False)
    estado = models.CharField(max_length=3,
                                choices=[('ON', 'ON'), ('OFF', 'OFF')],
                                default='ON')
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30, default='admin')
    fecha_modificacion = models.DateField(auto_now=True)
    
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
