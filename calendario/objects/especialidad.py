# -*- coding: utf-8 -*-
from django.db import models
from perfil.models import Institucion

class Especialidad(models.Model):
    
    nombre = models.CharField(max_length=100, null=False)
    carga_horaria_semanal = models.IntegerField(default=0, null=False)
    max_horas_diaria = models.IntegerField(default=0, null=False)
    color = models.CharField(max_length=10, default="#FFFFFF", null=False)
    estado = models.CharField(max_length=3,
                                choices=[('ON', 'ON'), ('OFF', 'OFF')],
                                default='ON')
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30, default='admin')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    institucion = models.ForeignKey(Institucion)
    
    @classmethod
    def create(cls, especialidad_id=0):
        
        if especialidad_id != 0:
            return Especialidad.objects.get(pk=especialidad_id)
        
        return Especialidad()
    
    def __str__(self, ):
        return self.nombre.encode('utf-8')
    
    def __repr__(self, ):
        return self.nombre.encode('utf-8')
    
    def __eq__(self, o):
        return self.nombre == o.nombre    
    
    def set_nombre(self, nombre):
        
        if nombre == "":
            raise Exception("El nombre no puede estar vacío.")
        
        self.nombre = nombre
    
    def set_carga_horaria_semanal(self, carga_horaria_semanal):
        
        if carga_horaria_semanal == "" or int(carga_horaria_semanal) < 1:
            raise Exception("La carga horaria semanal no puede ser menor a 1.")
        
        self.carga_horaria_semanal = carga_horaria_semanal
    
    def set_max_horas_diaria(self, max_horas_diaria):
        
        if max_horas_diaria == "" or int(max_horas_diaria) < 1:
            raise Exception("La horas diarias máxima no puede ser menor a 1.")
        
        self.max_horas_diaria = max_horas_diaria
    
