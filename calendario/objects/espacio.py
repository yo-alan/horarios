# -*- coding: utf-8 -*-
import sys
import copy
from random import randrange, randint

from django.db import models

from especialidad import Especialidad
from profesional import Profesional
from penalidad import Penalidad

PUNTOS_HORAS_SEMANALES = 1
CANT_PAREJAS = 4
PARTICIPANTES = 2

class Espacio(models.Model):
    """
    Clase que abarca el medio ambiente
    en el cual se desarrolla el algoritmo.
    
    @Atributos:
    .dias_habiles - lista con los dias a cubrir. Valor: [].
    .horas - lista con las horas a cubrir. Valor: [].
    .poblacion - lista de individuos. Valor: [].
    .coordinadores - lista de coordinadores. Valor: [].
    .tamanio_poblacion - tamaño de la población. Valor: 0.
    .grado - puntaje promedio de la población actual. Valor: 0.
    """
    
    ON = 1
    OFF = 2
    GENERANDO = 3
    
    nombre = models.CharField(max_length=100, null=False, blank=False, unique=True)
    estado = models.IntegerField(default=1, null=False)
    progreso = models.IntegerField(default=0, null=False)
    usuario_creador = models.CharField(max_length=30, default='admin')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificador = models.CharField(max_length=30,
                                            default='admin')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    especialidades = models.ManyToManyField(Especialidad)
    profesionales = models.ManyToManyField(Profesional)
    
    @classmethod
    def create(cls, espacio_id=0, tamanio_poblacion=0):
        
        espacio = None
        
        if espacio_id != 0:
            espacio = Espacio.objects.get(pk=espacio_id)
        else:
            espacio = Espacio()
        
        espacio._horas = []
        espacio._dias_habiles = []
        espacio._coordinadores = []
        espacio._poblacion = []
        espacio._tamanio_poblacion = tamanio_poblacion
        espacio._grado = 0
        
        puntos = Penalidad.create('RESTRICCION PROFESIONAL').puntos
        espacio.PUNTOS_RESTRICCION_PROFESIONAL = puntos
        
        puntos = Penalidad.create('HORAS DIARIAS').puntos
        espacio.PUNTOS_HORAS_DIARIAS = puntos
        
        puntos = Penalidad.create('DISTRIBUCION HORARIA').puntos
        espacio.PUNTOS_DISTRIBUCION_HORARIA = puntos
        
        from diaHabil import DiaHabil
        from calendario import Calendario
        
        for dia_habil in DiaHabil.objects.filter(espacio=espacio):
            espacio._dias_habiles.append(dia_habil)
        
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
        
        cant_horas = 0
        individuos = []
        
        # Iteramos generando todas las combinaciones de horarios
        # posibles. Y por cada uno creamos un calendario.
        
        # Contamos la cantidad total de horas.
        for coordinador in self.coordinadores:
            cant_horas += coordinador.especialidad.carga_horaria_semanal
        
        # Cantidad de iteraciones por los dias.
        for dia in self.dias_habiles:
            
            # Cantidad de iteraciones por las horas.
            for hora in self.horas:
                
                # Iteracion por cada coordinador.
                for coordinador in self.coordinadores:
                    
                    # Se crea un Calendario.
                    calendario = Calendario.create()
                    # Se le asigna este espacio.
                    calendario.espacio = self
                    # A su vez el Calendario es agregado a la poblacion.
                    individuos.append(calendario)
                    
                    # Se crea un Horario.
                    horario = Horario()
                    # Se le asigna el Coordinador.
                    horario.coordinador = coordinador
                    # Se le asigna una hora desde.
                    horario.hora_desde = hora.hora_desde
                    # Se le asigna una hora hasta.
                    horario.hora_hasta = hora.hora_hasta
                    # Se le asigna un dia de la semana.
                    horario.dia_semana = dia.dia
                    # El Horario es agregado al Calendario.
                    calendario.agregar_horario(horario)
                
                # La cantidad total de horas no fue cubierta, quiere
                # decir que en el calendario deben haber horas libres.
                if len(self.dias_habiles) * len(self.horas) != cant_horas:
                    
                    # Cantidad de iteraciones por los dias.
                    for dia in self.dias_habiles:
                        
                        # Cantidad de iteraciones por las horas.
                        for hora in self.horas:
                            
                            # Se crea un Calendario.
                            calendario = Calendario.create()
                            # Se le asigna este espacio.
                            calendario.espacio = self
                            # A su vez el Calendario es agregado a la poblacion.
                            individuos.append(calendario)
                            
                            # Se crea un Horario.
                            horario = Horario()
                            # Se le asigna una hora desde.
                            horario.hora_desde = hora.hora_desde
                            # Se le asigna una hora hasta.
                            horario.hora_hasta = hora.hora_hasta
                            # Se le asigna un dia de la semana.
                            horario.dia_semana = dia.dia
                            # El Horario es agregado al Calendario.
                            calendario.agregar_horario(horario)
        
        # Rellenamos los calendarios generando Horarios aleatoriamente.
        
        coordinadores_asig_global = []
        
        for coordinador in self.coordinadores.all():
            
            carga_horaria = coordinador.especialidad.carga_horaria_semanal
            
            for i in range(carga_horaria):
                
                coordinadores_asig_global.append(copy.copy(coordinador))
        
        for individuo in individuos:
            
            # Se crea la lista de coordinadores a asignar.
            coordinadores_asig = copy.copy(coordinadores_asig_global)
            
            for coordinador in coordinadores_asig_global:
                
                if coordinador == individuo.horarios[0][0].coordinador:
                    coordinadores_asig.remove(coordinador)
                    break
            
            horas_libres = abs(len(self.dias_habiles) * len(self.horas) - cant_horas)
            
            for i in range(horas_libres):
                
                coordinadores_asig.append(None)
                
            # Iteramos por la cantidad de dias.
            for dia in self.dias_habiles:
                
                # Tambien por la cantidad de horas.
                for hora in self.horas:
                    
                    if len(coordinadores_asig) == 0:
                        break
                    
                    indice = randint(0, len(coordinadores_asig)-1)
                    
                    coordinador = coordinadores_asig[indice]
                    
                    # Se crea un Horario.
                    horario = Horario()
                    # Se le asigna el Coordinador.
                    horario.coordinador = coordinador
                    # Se le asigna una hora desde.
                    horario.hora_desde = hora.hora_desde
                    # Se le asigna una hora hasta.
                    horario.hora_hasta = hora.hora_hasta
                    # Se le asigna un dia de la semana.
                    horario.dia_semana = dia.dia
                    
                    # Comprobamos que el Horario generado
                    # no exista en el Calendario.
                    existe = False
                    for franja_horaria in individuo.horarios:
                        for horario_comp in franja_horaria:
                            if horario == horario_comp:
                                existe = True
                    
                    # Si ya existia continuamos generando.
                    if existe:
                        continue
                    
                    coordinadores_asig.remove(coordinador)
                    
                    # Lo agregamos a la lista de horarios del Calendario.
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
        
        # Por cada individuo en la poblacion.
        for calendario in poblacion[:]:
            
            # Si el individuo no cumple la asignacion de horas semanales
            # es abortado.
            if self.asignacion_semanal(calendario) != 0:
                poblacion.remove(calendario)
                continue
            
            # Primera evaluacion: Se evalua que los horarios asignados
            # cumplan las restricciones del profesional que contienen.
            calendario.puntaje += self.asignacion_horaria(calendario)
            
            # Segunda evaluacion: Se busca que las especialidades
            # cumplan con la horas maximas por dia.
            calendario.puntaje += self.asignacion_diaria(calendario)
            
            # Tercera evaluación: En esta instancia se desea comprobar
            # la distribución horaria de las especialidades.
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
        
        # La division por 4 representa el número de parejas para cruzar.
        cantidad_parejas = len(self.poblacion) / CANT_PAREJAS
        
        while cantidad_parejas > len(parejas):
            
            pareja = self.seleccionar()
            
            # Damos vuelta la pareja para asegurarnos la evaluación.
            jarepa = (pareja[1], pareja[0])
            
            if pareja not in parejas and jarepa not in parejas:
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
        
        # Obtenemos cada pareja (padre y madre) del listado.
        for padre, madre in parejas:
            
            # Y los cruzamos. Almacenamos los hijos resultantes.
            poblacion_nueva += padre.crossover(madre)
        
        return poblacion_nueva
    
    def actualizarpoblacion(self, hijos):
        """
        Se realiza el reemplazo de padres por hijos. Se toma el peor
        mitad y es reemplazada por el total de hijos.
        
        @Parametros:
        hijos: list[Calendario].
        
        @Return:
        None.
        """
        
        # Dividimos la población a la mitad.
        punto_corte = len(self.poblacion) / 2
        
        irreemplazables = self.poblacion[:punto_corte]
        reemplazables = self.poblacion[punto_corte:]
        asignables = []
        
        # Aleatoriamente quitamos individuos de la peor mitad y los
        # reemplazamos por los hijos.
        for calendario in hijos:
            
            i = randint(0, len(reemplazables)-1)
            
            reemplazables.remove(reemplazables[i])
            
            asignables.append(calendario)
        
        self.poblacion = irreemplazables + reemplazables + asignables
        
        # Y por último ordenamos la población.
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
        
        # Por cada franja de horarios.
        for franja_horaria in calendario.horarios:
            
            # Por cada horario dentro de la franja.
            for horario in franja_horaria:
                
                # Si el horario no está bien asignado es penalizado.
                if not self.itswellassigned(horario):
                    puntos += self.PUNTOS_RESTRICCION_PROFESIONAL
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
        
        # Por cada especialidad en el espacio.
        for especialidad in self.especialidades.all():
            
            # Obtenemos la cantidad de horas semanales de la especialidad.
            horas_semanales = self.horas_semanales_de(especialidad, calendario)
            
            puntos += horas_semanales * PUNTOS_HORAS_SEMANALES
            
            if puntos > 0:
                return puntos
        
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
                    
                    # Obtenemos el horario a evaluar.
                    horario = calendario.horarios[i][j]
                    
                    if horario.coordinador == None:
                        continue
                    
                    if especialidad == horario.coordinador.especialidad:
                        horas_diarias += 1
                
                # Si la especialidad se exedio en la asignacion diaria.
                if especialidad.max_horas_diaria < horas_diarias:
                    
                    # Se penaliza de acuerdo a la cantidad de horas
                    # que se exedio.
                    horas_penalizar = (horas_diarias - especialidad.max_horas_diaria)
                    
                    puntos += horas_penalizar * self.PUNTOS_HORAS_DIARIAS            
        
        return puntos
    
    def distribucion_horaria(self, calendario):
        """
        Función que determina la distribución de horarios dentro
        de un calendario.
        
        @Parametros:
        calendario: Calendario.
        
        @Return:
        int.
        """
        
        puntos = 0
        
        for j in range(len(self.dias_habiles)):
            
            for i in range(len(self.horas)-2):
                
                # Obtenemos los 3 horarios a comparar.
                horario_anterior = calendario.horarios[i][j]
                horario = calendario.horarios[i+1][j]
                horario_siguiente = calendario.horarios[i+2][j]
                
                if horario_anterior.coordinador != horario.coordinador:
                    if horario.coordinador != horario_siguiente.coordinador:
                        puntos += self.PUNTOS_DISTRIBUCION_HORARIA
            
            horario_1 = calendario.horarios[0][j]
            horario_2 = calendario.horarios[1][j]
            
            # Evaluamos el extremo inicial.
            if horario_1.coordinador != horario_2.coordinador:
                puntos += self.PUNTOS_DISTRIBUCION_HORARIA
            
            horario_1 = calendario.horarios[i+1][j]
            horario_2 = calendario.horarios[i+2][j]
            
            # Evaluamos el extremo final.
            if horario_1.coordinador != horario_2.coordinador:
                puntos += self.PUNTOS_DISTRIBUCION_HORARIA
        
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
        
        if horario.coordinador == None:
            return
        
        # Por cada restriccion del profesional.
        for restriccion in horario.coordinador.profesional.restricciones.all():
            
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
        
        # Contador de horas semanales.
        horas_semanales = 0
        
        # Por cada franja de horarios.
        for franja_horaria in calendario.horarios:
            
            # Por cada horario en la franja horaria.
            for horario in franja_horaria:
                
                if horario.coordinador == None:
                    continue
                
                # Si la especialidad es igual, contamos.
                if horario.coordinador.especialidad == especialidad:
                    horas_semanales += 1
        
        return abs(especialidad.carga_horaria_semanal - horas_semanales)
    
    def seleccionar(self, ):
        """
        Función encargada de seleccionar dos padres para su cruce.
        Método de selección elegido: Torneo deterministico.
        
        @Return:
        tuple(Calendario, Calendario).
        """
        
        padre = None
        madre = None
        
        # Los elegidos para competir.
        elegidos = []
        
        # Seleccionamos los individuos para el torneo aleatoriamente.
        for i in range(PARTICIPANTES):
            
            indice = randrange(len(self.poblacion))
            
            calendario = self.poblacion[indice]
            
            if calendario not in elegidos:
                elegidos.append(calendario)
        
        # Obtenemos al primer ganador.
        padre = self.winneroftournament(elegidos)
        
        while madre != padre:
            
            elegidos = []
            
            for i in range(PARTICIPANTES):
                
                indice = randrange(len(self.poblacion))
                
                calendario = self.poblacion[indice]
                
                if calendario not in elegidos:
                    elegidos.append(calendario)
            
            # Obtenemos al segundo ganador.
            madre = self.winneroftournament(elegidos)
        
        return (padre, madre)
    
    def winneroftournament(self, elegidos):
        """
        Función que retorna al ganador de un torneo entre los
        individuos elegidos dicho certamen.
        
        @Parametros:
        elegidos: Calendario[].
        
        @Return:
        Calendario.
        """
        
        while len(elegidos) != 1:
            
            i = 0
            j = 0
            
            while i != j:
                i = randrange(len(elegidos))
                j = randrange(len(elegidos))
            
            calendario1 = elegidos[i]
            calendario2 = elegidos[j]
            
            if calendario1 < calendario2:
                elegidos.remove(calendario1)
            else:
                elegidos.remove(calendario2)
        
        return elegidos[0]
    
    def esHoraValida(self, la_hora):
        
        # Verificamos que no se solape con alguna ya cargada.
        for hora in self.horas:
            
            if hora.hora_desde <= la_hora.hora_desde < hora.hora_hasta:
                return False
            
            if hora.hora_desde < la_hora.hora_hasta <= hora.hora_hasta:
                return False
        
        return True
    
    @property
    def tamanio_poblacion(self, ):
        return self._tamanio_poblacion
    
    @tamanio_poblacion.setter
    def tamanio_poblacion(self, tamanio_poblacion):
        self._tamanio_poblacion = tamanio_poblacion
    
    @property
    def poblacion(self, ):
        try:
            return self._poblacion
        except AttributeError:
            
            from calendario import Calendario
            
            self._poblacion = []
            
            for calendario in Calendario.objects.filter(espacio=self):
                
                calendario = Calendario.create(calendario.id)
                
                self._poblacion.append(calendario)
            
            return self._poblacion
    
    @poblacion.setter
    def poblacion(self, poblacion):
        self._poblacion = poblacion
    
    @property
    def horas(self, ):
        from hora import Hora
        
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
    def grado(self, ):
        
        suma = sum(calendario.puntaje for calendario in self.poblacion)
        
        return suma / len(self.poblacion)
