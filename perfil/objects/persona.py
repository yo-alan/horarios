# -*- coding: utf-8 -*-
from django.db import models

def purificador(nombre):
    
    nombre_copia = nombre
    
    nombre = ""
    
    for n in nombre_copia.split(' '):
        
        if not n.isalpha():
            raise
        
        nombre = nombre + " " + n.capitalize()
    
    if nombre.startswith(' '):
        nombre = nombre[1:]
    
    return nombre

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

class Persona(models.Model):
    
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    cuil = models.CharField(max_length=13, null=False, blank=False)
    genero = models.CharField(max_length=1,
                                choices=[('F', 'F'), ('M', 'M')],
                                default='F')
    estado = models.CharField(max_length=3,
                                choices=[('ON', 'ON'), ('OFF', 'OFF')],
                                default='ON')
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30, default='admin')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self, ):
        return (self.apellido + ", " + self.nombre).encode('utf-8')
    
    def __eq__(self, o):
        return self.cuil == o.cuil
    
    def set_nombre(self, nombre):
        
        if nombre == "":
            raise Exception("El nombre no puede estar vacío.")
        
        try:
            nombre = purificador(nombre)
        except:
            raise Exception("El nombre posee caracteres no permitidos.")
        
        self.nombre = nombre
    
    def set_apellido(self, apellido):
        
        if apellido == "":
            raise Exception("El apellido no puede estar vacío.")
        
        try:
            apellido = purificador(apellido)
        except:
            raise Exception("El apellido posee caracteres no permitidos.")
        
        self.apellido = apellido
    
    def set_cuil(self, cuil):
        
        if not esCUITValida(cuil):
            raise Exception("El cuil no es válido.")
        
        self.cuil = cuil
    
    def set_fecha_nacimiento(self, fecha_nacimiento):
        
        if fecha_nacimiento == "":
            raise Exception("La fecha de nacimiento no es válida.")
        
        self.fecha_nacimiento = fecha_nacimiento
    
    def set_genero(self, genero):
        
        self.genero = genero
