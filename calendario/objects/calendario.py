# -*- coding: utf-8 -*-
import copy
import random

from django.db import models

from espacio import Espacio

class Calendario(models.Model):
    
    espacio = models.ForeignKey(Espacio)
    puntaje = models.IntegerField(default=0)
    estado = models.CharField(max_length=3,
                                choices=[('ON', 'ON'), ('OFF', 'OFF')],
                                default='ON')
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30, default='admin')
    fecha_modificacion = models.DateField(auto_now=True)
    
    @classmethod
    def create(cls, calendario_id=0):
        
        calendario = None
        
        if calendario_id != 0:
            calendario = Calendario.objects.get(pk=calendario_id)
        else:
            calendario = Calendario()
        
        calendario._horarios = []
        
        return calendario
    
    def __str__(self, ):
        return str(self.espacio) + "(" + str(self.id) + ")"
    
    def cruce(self, madre, prob_mutacion=0.01):
        """
        Cruza este individuo con otro del mismo tipo y retorna la
        cantidad de hijos resultantes.
        
        @Parametros:
        madre: Calendario.
        prob_mutacion: float.
        
        @Return:
        Calendario[].
        """
        
        if not isinstance(madre, Calendario):
            raise Exception("Se esperaba un Calendario.")
        
        if self == madre:
            return []
        
        hijos = []
        
        #Obtenemos el punto de corte dividiendo en 2 la cantidad
        #de horarios.
        puntos_corte = len(self.horarios)
        
        hijo1 = Calendario.create()
        
        hijo1.espacio = self.espacio
        
        for i in range(puntos_corte):
            
            if i % 2 == 0:
                for horario in self.horarios[i:i+1][0]:
                    hijo1.agregar_horario(copy.copy(horario))
            else:
                for horario in madre.horarios[i:i+1][0]:
                    hijo1.agregar_horario(copy.copy(horario))
        
        if prob_mutacion > random.random():
            hijo1.mutar()
        
        #Segundo hijo.
        
        hijo2 = Calendario.create()
        
        hijo2.espacio = self.espacio
        
        for i in range(puntos_corte):
            
            if i % 2 != 0:
                for horario in self.horarios[i:i+1][0]:
                    hijo2.agregar_horario(copy.copy(horario))
            else:
                for horario in madre.horarios[i:i+1][0]:
                    hijo2.agregar_horario(copy.copy(horario))
        
        if prob_mutacion > random.random():
            hijo2.mutar()
        
        #Tercer hijo.
        
        #~ hijo3 = Calendario.create()
        #~ 
        #~ hijo3.espacio = self.espacio
        #~ 
        #~ for franja_horaria in madre.horarios[:punto_corte]:
            #~ for horario in franja_horaria:
                #~ hijo3.agregar_horario(copy.copy(horario))
        #~ 
        #~ for franja_horaria in self.horarios[punto_corte:]:
            #~ for horario in franja_horaria:
                #~ hijo3.agregar_horario(copy.copy(horario))
        #~ 
        #~ for franja_horaria in madre.horarios[punto_corte2:]:
            #~ for horario in franja_horaria:
                #~ hijo3.agregar_horario(copy.copy(horario))
        #~ 
        #~ if prob_mutacion > random.random():
            #~ hijo2.mutar()
        
        hijos.append(hijo1)
        hijos.append(hijo2)
        #~ hijos.append(hijo3)
        
        return hijos
    
    def mutar(self, ):
        
        i = random.randint(0, len(self.horarios)-1)
        j = random.randint(0, len(self.horarios[0])-1)
        
        k = random.randint(0, len(self.horarios)-1)
        l = random.randint(0, len(self.horarios[0])-1)
        
        primero = self.horarios[i][j]
        segundo = self.horarios[k][l]
        
        especialidad_aux = primero.especialidad
        profesional_aux = primero.profesional
        
        primero.especialidad = segundo.especialidad
        primero.profesional = segundo.profesional
        
        segundo.especialidad = especialidad_aux
        segundo.profesional = profesional_aux
    
    def agregar_horario(self, horario):
        """
        Agrega un Horario a la lista de horarios del Calendario.
        
        @Parametros:
        horario: Horario.
        
        @Return:
        None.
        """
        
        #Por cada franja horaria.
        for franja_horaria in self._horarios:
            
            #Si contiene un Horario con misma
            #hora_desde lo agrega a la lista.
            if franja_horaria[0].hora_desde == horario.hora_desde:
                
                #Lo agregamos al final.
                franja_horaria.append(horario)
                
                #Ordenamos la lista.
                franja_horaria.sort()
                
                return None
        
        #Por cada franja horaria.
        for franja_horaria in copy.copy(self._horarios):
            
            #Ubicamos la nueva franja horaria donde corresponda.
            if horario.hora_desde < franja_horaria[0].hora_desde:
                
                indice = self._horarios.index(franja_horaria)
                
                #Insertamoe el horario creando una nueva franja horaria.
                self._horarios.insert(indice, [horario])
                
                return None
        
        #Si horarios esta vacio se agrega el horario sin problemas.
        self._horarios.append([horario])
    
    def full_save(self, ):
        
        #Se guarda el mismo para obtener una ID de la BBDD.
        self.save()
        
        #Por cada franja horaria.
        for franja_horaria in self.horarios:
            
            #Guarda todos y cada uno de los horarios que posee.
            for horario in franja_horaria:
                horario.calendario = self
                horario.save()
    
    @property
    def horarios(self, ):
        from horario import Horario
        
        if not self._horarios:
            horarios = Horario.objects.filter(calendario=self)\
                                        .order_by('hora_desde', 'dia_semana')
            
            for horario in horarios:
                self.agregar_horario(horario)
        
        return self._horarios
    
    @horarios.setter
    def horarios(self, horarios):
        self._horarios = horarios
    
    def __lt__(self, o):
        return self.puntaje < o.puntaje
    
    def __le__(self, o):
        return self.puntaje <= o.puntaje
    
    def __gt__(self, o):
        return self.puntaje > o.puntaje
    
    def __ge__(self, o):
        return self.puntaje >= o.puntaje
