# -*- coding: utf-8 -*-
from django.db import models

def purificador(nombre):
    
    nombre_copia = nombre
    
    nombre = ""
    
    for n in nombre_copia.split(' '):
        
        if not n.isalpha():
            raise
        
        nombre = nombre + " " + n
    
    if nombre.startswith(' '):
        nombre = nombre[1:]
    
    return nombre

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
    
    def setnombre(self, nombre):
        
        if nombre == "":
            raise Exception("El nombre no puede estar vacío.")
        
        try:
            nombre = purificador(nombre)
        except:
            raise Exception("El nombre posee caracteres no permitidos.")
        
        self.nombre = nombre
    
    def setcarga_horaria_semanal(self, carga_horaria_semanal):
        
        if carga_horaria_semanal == "" or int(carga_horaria_semanal) < 1:
            raise Exception("La carga horaria semanal no puede ser menor a 1.")
        
        self.carga_horaria_semanal = carga_horaria_semanal
    
    def setmax_horas_diaria(self, max_horas_diaria):
        
        if max_horas_diaria == "" or int(max_horas_diaria) < 1:
            raise Exception("La horas diarias máxima no puede ser menor a 1.")
        
        self.max_horas_diaria = max_horas_diaria
    
