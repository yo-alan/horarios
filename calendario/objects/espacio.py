# -*- coding: utf-8 -*-
import sys
import copy
from random import randrange, randint

from django.db import models

from especialidad import Especialidad
from profesional import Profesional

PUNTOS_RESTRICCION_PROFESIONAL = 0
PUNTOS_HORAS_SEMANALES = 1
PUNTOS_HORAS_DIARIAS = 1
PUNTOS_DISTRIBUCION_HORARIA = 4

class Espacio(models.Model):
    """
    Clase que abarca el medio ambiente
    en el cual se desarrolla el algoritmo.
    
    @Atributos:
    .dias_habiles - lista con los dias a cubrir. Valor: {}.
    .horarios - diccionario con los horarios a cubrir. Valor: {}.
    .poblacion - lista de individuos. Valor: [].
    .generaciones - cantidad de generaciones a generar. Valor: 0.
    """
    
    nombre = models.CharField(max_length=100, null=False, blank=False)
    estado = models.CharField(max_length=3,
                                choices=[('ON', 'ON'), ('OFF', 'OFF')],
                                default='ON')
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30,
                                            default='admin')
    fecha_modificacion = models.DateField(auto_now=True)
    
    especialidades = models.ManyToManyField(Especialidad)
    profesionales = models.ManyToManyField(Profesional)
    
    @classmethod
    def create(cls, espacio_id=0, generaciones=0):
        
        espacio = None
        
        if espacio_id != 0:
            espacio = Espacio.objects.get(pk=espacio_id)
        else:
            espacio = Espacio()
        
        espacio._calendarios = []
        espacio._horas = []
        espacio._coordinadores = []
        espacio._poblacion = []
        espacio._generaciones = generaciones
        
        #HARDCODED
        espacio._dias_habiles = [1, 2, 3, 4, 5]
        
        return espacio
    
    def __str__(self, ):
        return unicode(self.nombre)
    
    def setnombre(self, nombre):
        
        if nombre == "":
            raise Exception("El nombre no puede estar vacío.")
        
        self.nombre = nombre
    
    # GENETIC ALGORITHMS
    
    def generarpoblacioninicial(self, ):
        """
        Genera individuos desde cero y
        los guarda en el atributo 'poblacion'.
        
        @Parametros:
        None.
        
        @Return:
        None.
        """
        from calendario import Calendario
        from horario import Horario
        
        #Iteramos generando todas las combinaciones de horarios
        #posibles. Y agregamos cada uno a un calendario.
        
        individuos = []
        
        #Cantidad de iteraciones por los dias.
        for dia in self.dias_habiles:
            
            #Cantidad de iteraciones por los horarios.
            for hora in self.horas:
                
                #Iteracion por cada coordinador.
                for coordinador in self.coordinadores:
                    
                    #Se crea un Calendario.
                    calendario = Calendario.create()
                    #Se le asigna este espacio.
                    calendario.espacio = self
                    #A su vez el Calendario es agregado a la poblacion.
                    individuos.append(calendario)
                    
                    #Se crea un Horario.
                    horario = Horario()
                    #Se le asigna una Especialidad.
                    horario.especialidad = coordinador.especialidad
                    #Se le asigna una Profesional.
                    horario.profesional = coordinador.profesional
                    #Se le asigna una hora desde.
                    horario.hora_desde = hora.hora_desde
                    #Se le asigna una hora hasta.
                    horario.hora_hasta = hora.hora_hasta
                    #Se le asigna un dia de la semana.
                    horario.dia_semana = dia
                    #El Horario es agregado al Calendario.
                    calendario.agregar_horario(horario)
                    
        
        #Rellenamos el Calendario generando Horarios.
        
        coordinadores_asig_global = []
        
        for coordinador in self.coordinadores.all():
            
            carga_horaria = coordinador.especialidad.carga_horaria_semanal
            
            for i in range(carga_horaria):
                
                coordinadores_asig_global.append(copy.copy(coordinador))
        
        for individuo in individuos:
            
            coordinadores_asig = copy.copy(coordinadores_asig_global)
            
            for coordinador in coordinadores_asig_global:
                
                especialidad = individuo.horarios[0][0].especialidad
                
                if coordinador.especialidad == especialidad:
                    coordinadores_asig.remove(coordinador)
                    break
            
            #Iteramos por la cantidad de dias.
            for dia in self.dias_habiles:
                
                #Tambien por la cantidad de horarios.
                for hora in self.horas:
                    
                    if len(coordinadores_asig) == 0:
                        break
                    
                    indice = randint(0, len(coordinadores_asig)-1)
                    
                    coordinador = coordinadores_asig[indice]
                    
                    #Se crea un Horario.
                    horario = Horario()
                    #Se le asigna una Especialidad.
                    horario.especialidad = coordinador.especialidad
                    #Se le asigna una Profesional.
                    horario.profesional = coordinador.profesional
                    #Se le asigna una hora desde.
                    horario.hora_desde = hora.hora_desde
                    #Se le asigna una hora hasta.
                    horario.hora_hasta = hora.hora_hasta
                    #Se le asigna un dia de la semana.
                    horario.dia_semana = dia
                    
                    #Comprobamos que el Horario generado
                    #no exista en el Calendario.
                    existe = False
                    for franja_horaria in individuo.horarios:
                        for horario_comp in franja_horaria:
                            if horario == horario_comp:
                                existe = True
                    
                    #Si ya existia continuamos generando.
                    if existe:
                        continue
                    
                    coordinadores_asig.remove(coordinador)
                    
                    #Lo agregamos a la lista de horarios del Calendario.
                    individuo.agregar_horario(horario)
            
            self.poblacion.append(individuo)
    
    def fitness(self, poblacion):
        """
        Asigna un puntaje a los calendarios.
        Utiliza las restricciones de los profesionales, de las
        especialidades y la distribucion horaria para determinar
        el valor de aptitud de los individuos.
        
        @Parametros:
        None.
        
        @Return:
        None.
        """
        
        #Por cada individuo en la poblacion.
        for calendario in poblacion[:]:
            
            #Si el individuo no cumple la asignacion de horas semanales
            #es abortado.
            if self.asignacion_semanal(calendario) != 0:
                poblacion.remove(calendario)
                continue
            
            #Primera evaluacion: Se evalua que los horarios asignados
            #cumplan las restricciones del profesional que contienen.
            calendario.puntaje += self.asignacion_horaria(calendario)
            
            #Segunda evaluacion: Se busca que las especialidades
            #cumplan con la horas maximas por dia.
            calendario.puntaje += self.asignacion_diaria(calendario)
            
            #Tercera evaluación: En esta instancia se desea comprobar
            #la distribución horaria de las especialidades.
            calendario.puntaje += self.distribucion_horaria(calendario)
    
    def seleccion(self, ):
        """
        Retorna el 50% de individuos de la población
        total para el cruce.
        
        @Parametros:
        None.
        
        @Return:
        list.
        """
        
        parejas = []
        
        #La division por 4 representa el número de parejas para cruzar.
        cantidad_parejas = len(self.poblacion)/4
        
        while cantidad_parejas > len(parejas):
            
            pareja = self.seleccionar()
            
            if pareja not in parejas:
                parejas.append(pareja)
        
        return parejas
    
    def cruzar(self, parejas):
        """
        Genera una nueva población cruzando las parejas
        que recibe por parametros.
        
        @Parametros:
        parejas: list[tuple]
        
        @Return:
        list[Calendario].
        """
        
        poblacion_nueva = []
        
        #Obtenemos cada pareja (padre y madre) del listado.
        for padre, madre in parejas:
            
            #Y los cruzamos. Almacenamos los hijos resultantes.
            poblacion_nueva += padre.cruce(madre)
        
        return poblacion_nueva
    
    def actualizarpoblacion(self, hijos):
        """
        
        
        """
        
        punto_corte = len(self.poblacion) / 2
        
        irreemplazables = self.poblacion[:punto_corte]
        reemplazables = self.poblacion[punto_corte:]
        asignables = []
        
        for calendario in hijos:
            
            i = randint(0, len(reemplazables)-1)
            
            reemplazables.remove(reemplazables[i])
            
            asignables.append(calendario)
        
        self.poblacion = irreemplazables + reemplazables + asignables
        
        self.poblacion.sort()
    
    def asignacion_horaria(self, calendario):
        """
        Recorre el calendario contando los horarios mal asignados,
        este valor final se retorna.
        
        @Parametros:
        calendario: Calendario.
        
        @Return:
        int.
        """
        
        puntos = 0
        
        #Por cada franja de horarios.
        for franja_horaria in calendario.horarios:
            
            #Por cada horario dentro de la franja.
            for horario in franja_horaria:
                
                #Si el horario no está bien asignado es penalizado.
                if not self.itswellassigned(horario):
                    puntos += PUNTOS_RESTRICCION_PROFESIONAL
                    horario.penalizado += 1
        
        return puntos
    
    def asignacion_semanal(self, calendario):
        """
        Calcula los puntos del calendario comprobando que tanto
        se respetan las restricciones de horas semanales de las
        especialidades del espacio.
        
        @Parametros:
        calendario: Calendario.
        
        @Return:
        int.
        """
        
        puntos = 0
        
        #Por cada especialidad en el espacio.
        for especialidad in self.especialidades.all():
            
            #Obtenemos la cantidad de horas semanales de la especialidad.
            horas_semanales = self.horas_semanales_de(especialidad, calendario)
            
            puntos += horas_semanales * PUNTOS_HORAS_SEMANALES
        
        return puntos
    
    def asignacion_diaria(self, calendario):
        """
        Cuenta la cantidad de excesos de horas diaria de cada
        especialidad y se retorna el total.
        
        @Parametros:
        calendario: Calendario.
        
        @Return:
        int.
        """
        
        puntos = 0
        
        for especialidad in self.especialidades.all():
            
            for j in range(len(self.dias_habiles)):
                
                horas_diarias = 0
                
                for i in range(len(self.horas)):
                    
                    #Obtenemos el horario a evaluar.
                    horario = calendario.horarios[i][j]
                    
                    if especialidad == horario.especialidad:
                        horas_diarias += 1
                
                if especialidad.max_horas_diaria < horas_diarias:
                    
                    horas_penalizar = (horas_diarias - especialidad.max_horas_diaria)
                    
                    puntos += horas_penalizar * PUNTOS_HORAS_DIARIAS            
        
        return puntos
    
    def distribucion_horaria(self, calendario):
        """
        
        @Parametros:
        calendario: Calendario.
        
        @Return:
        int.
        """
        
        puntos = 0
        
        for j in range(len(self.dias_habiles)):
            
            for i in range(len(self.horas)-2):
                
                #Obtenemos los 3 horarios a comparar.
                horario_anterior = calendario.horarios[i][j]
                horario = calendario.horarios[i+1][j]
                horario_siguiente = calendario.horarios[i+2][j]
                
                if horario_anterior.especialidad != horario.especialidad:
                    if horario.especialidad != horario_siguiente.especialidad:
                        puntos += PUNTOS_DISTRIBUCION_HORARIA
            
            horario_1 = calendario.horarios[0][j]
            horario_2 = calendario.horarios[1][j]
            
            #Evaluamos el extremo inicial.
            if horario_1.especialidad != horario_2.especialidad:
                puntos += PUNTOS_DISTRIBUCION_HORARIA
            
            horario_1 = calendario.horarios[i+1][j]
            horario_2 = calendario.horarios[i+2][j]
            
            #Evaluamos el extremo final.
            if horario_1.especialidad != horario_2.especialidad:
                puntos += PUNTOS_DISTRIBUCION_HORARIA
        
        return puntos
    
    def itswellassigned(self, horario):
        """
        Verifica que la posición del horario dentro de el
        calendario no se superponga con ninguna restriccion
        del profesional dueño de dicho horario.
        
        @Parametros:
        horario: Horario.
        
        @Return:
        boolean.
        """
        
        #Validar que se reciba un Horario por parámetro.
        #~ if not isinstance(horario, Horario):
            #~ raise Exception("Se esperaba un Horario.")
        
        #Por cada restriccion del profesional.
        for restriccion in horario.profesional.restricciones.all():
            
            #Si no es el mismo dia de la semana del horario continuamos.
            if horario.dia_semana != restriccion.dia_semana:
                if restriccion.dia_semana != 7:
                    continue
            
            if (horario.hora_desde >= restriccion.hora_desde and horario.hora_desde < restriccion.hora_hasta):
                return False
            
            if (horario.hora_hasta > restriccion.hora_desde and horario.hora_hasta <= restriccion.hora_hasta):
                return False
            
            if (horario.hora_desde <= restriccion.hora_desde and horario.hora_hasta >= restriccion.hora_hasta):
                return False
            
            if (horario.hora_desde > restriccion.hora_desde and horario.hora_hasta < restriccion.hora_hasta):
                return False
            
            #Este if esta de mas?
            if (horario.hora_desde == restriccion.hora_desde and horario.hora_hasta == restriccion.hora_hasta):
                return False
            
        return True
    
    def horas_semanales_de(self, especialidad, calendario):
        """
        Cuenta la cantidad de horarios en el calendario que
        estén asignados a la especialidad que se recibe.
        Retorna un entero positivo que indica la cantidad de
        horas excedidas o faltantes de la especialidad semanalmente.
        
        @Parametros:
        calendario: Calendario.
        especialidad: Especialidad.
        
        @Return:
        Int.
        """
        
        #Validar que se reciba una Especialidad por parámetro.
        #~ if not isinstance(especialidad, Especialidad):
            #~ raise Exception("Se esperaba una Especialidad.")
        
        #Validar que se reciba un Calendario por parámetro.
        #~ if not isinstance(calendario, Calendario):
            #~ raise Exception("Se esperaba un Calendario.")
        
        #Contador de horas semanales.
        horas_semanales = 0
        
        #Por cada franja de horarios.
        for franja_horaria in calendario.horarios:
            
            #Por cada horario en la franja horaria.
            for horario in franja_horaria:
                
                #Si la especialidad es igual, contamos.
                if horario.especialidad == especialidad:
                    horas_semanales += 1
        
        return abs(especialidad.carga_horaria_semanal - horas_semanales)
    
    def seleccionar(self, ):
        """
        
        
        @Return:
        tuple(Calendario, Calendario).
        """
        
        padre = None
        madre = None
        
        #Los elegidos para competir.
        elegidos = []
        
        #Hacemos un torneo de 20 individuos.
        for i in range(20):
            
            indice = randrange(len(self.poblacion))
            
            calendario = self.poblacion[indice]
            
            if calendario not in elegidos:
                elegidos.append(calendario)
        
        padre = self.winneroftournament(elegidos)
        
        #~ while madre != padre:
        
        elegidos = []
        
        for i in range(20):
            
            indice = randrange(len(self.poblacion))
            
            calendario = self.poblacion[indice]
            
            if calendario not in elegidos:
                elegidos.append(calendario)
        
        madre = self.winneroftournament(elegidos)
        
        return (padre, madre)
    
    def winneroftournament(self, elegidos):
        """
        Funcion que retorna al ganador de un torneo entre los
        individuos elegidos.
        
        @Parametros:
        elegidos: Calendario[].
        
        @Return:
        calendario: Calendario.
        """
        
        while len(elegidos) != 1:
            
            calendario1 = elegidos[randrange(len(elegidos))]
            calendario2 = elegidos[randrange(len(elegidos))]
            
            if calendario1 < calendario2:
                elegidos.remove(calendario1)
            elif calendario1 > calendario2:
                elegidos.remove(calendario2)
            else:
                elegidos.remove(calendario2)
            
        return elegidos[0]
    
    @property
    def generaciones(self, ):
        return self._generaciones
    
    @generaciones.setter
    def generaciones(self, generaciones):
        self._generaciones = generaciones
    
    @property
    def poblacion(self, ):
        return self._poblacion
    
    @poblacion.setter
    def poblacion(self, poblacion):
        self._poblacion = poblacion
    
    @property
    def horas(self, ):
        from hora import Hora
        
        if not self._horas:
            self._horas = Hora.objects.filter(espacio=self)\
                                        .order_by('hora_desde')
        
        return self._horas
    
    @property
    def coordinadores(self, ):
        from coordinador import Coordinador
        
        if not self._coordinadores:
            self._coordinadores = Coordinador.objects.filter(espacio=self)\
                                                        .order_by('especialidad')
        
        return self._coordinadores
    
    @property
    def dias_habiles(self, ):
        return self._dias_habiles
    
    @property
    def calendarios(self, ):
        from calendario import Calendario
        
        if not self._calendarios:
            self._calendarios = Calendario.objects.filter(espacio=self)
        
        return self._calendarios
    
