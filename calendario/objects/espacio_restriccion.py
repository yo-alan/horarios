# -*- coding: utf-8 -*-
from django.db import models
from restriccion import Restriccion
from espacio import Espacio

class Espacio_restriccion(Restriccion):
	
	espacio = models.ForeignKey(Espacio)

