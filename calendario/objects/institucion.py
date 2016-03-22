# -*- coding: utf-8 -*-
from django.db import models

class Institucion(models.Model):
    
    nombre = models.CharField(max_length=100)
