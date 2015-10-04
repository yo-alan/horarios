# -*- coding: utf-8 -*-
from django.db import models

from persona import Persona
from especialidad import Especialidad

class Profesional(Persona):
    
    especialidades = models.ManyToManyField(Especialidad)
    
    @classmethod
    def create(cls, profesional_id=0):
        
        profesional = None
        
        if profesional_id != 0:
            profesional = Profesional.objects.get(pk=profesional_id)
        else:
            profesional = Profesional()
        
        profesional._restricciones = []
        
        return profesional
    
    @property
    def restricciones(self, ):
        from profesionalRestriccion import ProfesionalRestriccion
        
        return ProfesionalRestriccion.objects.filter(profesional=self)\
                                                .order_by('dia_semana', 'hora_desde')
