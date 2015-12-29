from django.db import models

# Create your models here.

class Actividad(models.Model):
    
    fecha = models.DateTimeField(auto_now_add=True)
    mensaje = models.CharField(max_length=100)
    usuario = models.CharField(max_length=30, default='admin')
