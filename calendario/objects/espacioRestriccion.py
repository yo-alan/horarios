# -*- coding: utf-8 -*-
from django.db import models

from restriccion import Restriccion
from espacio import Espacio

class EspacioRestriccion(Restriccion):
    
    espacio = models.ForeignKey(Espacio)

