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

class Persona(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	apellido = models.CharField(max_length=100, null=False, blank=False)
	cuil = models.CharField(max_length=11, unique=True, null=False, blank=False)
	
	def setnombre(self, nombre):
		
		if nombre == "":
			raise Exception("El nombre no puede estar vacío.")
		
		try:
			nombre = purificador(nombre)
		except:
			raise Exception("El nombre posee caracteres no permitidos.")
		
		self.nombre = nombre
	
	def setapellido(self, apellido):
		
		if apellido == "":
			raise Exception("El apellido no puede estar vacío.")
		
		try:
			apellido = purificador(apellido)
		except:
			raise Exception("El apellido posee caracteres no permitidos.")
		
		self.apellido = apellido
	
	def setcuil(self, cuil):
		
		if cuil == "":
			raise Exception("El cuil no puede estar vacío.")
		
		self.cuil = cuil
