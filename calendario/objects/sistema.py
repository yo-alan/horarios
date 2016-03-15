# -*- coding: utf-8 -*-
from django.db import models

class Sistema(models.Model):
    
    estado = models.CharField(max_length=3,
                                choices=[('GENERANDO', 'GENERANDO'),
                                        ('IDLE', 'IDLE')],
                                default='IDLE')
