# -*- coding: utf-8 -*-
from django.db import models

class Persona(models.Model):
	
	nombre = models.CharField(max_length=100, null=False, blank=False)
	apellido = models.CharField(max_length=100, null=False, blank=False)
	cuil = models.CharField(max_length=11, unique=True, null=False, blank=False)
