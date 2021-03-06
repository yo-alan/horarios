# -*- coding: utf-8 -*-
from django.db import models

def esCUITValida(cuit):
    
    cuit = str(cuit)
    cuit = cuit.replace("-", "")
    cuit = cuit.replace(" ", "")
    cuit = cuit.replace(".", "")
    
    if len(cuit) != 11:
        return False
    
    if not cuit.isdigit():
        return False
    
    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    aux = 0
    for i in xrange(10):
        aux += int(cuit[i]) * base[i]
    
    aux = 11 - (aux % 11)
    
    if aux == 11:
        aux = 0
    elif aux == 10:
        aux = 9
    
    if int(cuit[10]) == aux:
        return True
    else:
        return False

class Institucion(models.Model):
    
    ACTIVA = 1
    ANUALDA = 2
    
    nombre = models.CharField(max_length=100, null=False, blank=False)
    cuil = models.CharField(max_length=13, null=False, blank=False)
    direccion = models.CharField(max_length=100, null=False, blank=False)
    estado = models.IntegerField(choices=[(ACTIVA, ACTIVA), (ANUALDA, ANUALDA)],
                                default=ACTIVA)
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30,
                                            default='admin')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    def set_nombre(self, nombre):
        
        if nombre == '':
            raise Exception("El nombre no puede estar vacío.")
        
        self.nombre = nombre
    
    def set_direccion(self, direccion):
        
        if direccion == '':
            raise Exception("La dirección no puede estar vacía.")
        
        self.direccion = direccion
    
    def set_cuil(self, cuil):
        
        if not esCUITValida(cuil):
            raise Exception("El cuil no es válido.")
        
        self.cuil = cuil
    
