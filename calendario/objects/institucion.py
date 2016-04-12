# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group

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

class Institucion(Group):
    
    cuil = models.CharField(max_length=13, null=False, blank=False)
    direccion = models.CharField(max_length=100, null=False, blank=False)
