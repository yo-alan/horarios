# -*- coding: utf-8 -*-
from django.db import models
from restriccion import Restriccion
from profesional import Profesional

class Profesional_restriccion(Restriccion):
	
	profesional = models.ForeignKey(Profesional)
