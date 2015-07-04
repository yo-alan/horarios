*Horarios*
========

***Práctica Profesional/Trabajo Final Integrador 2015 - UDC***

Es una aplicación que permite la organización de horarios y la asignación de los mismos a profesionales que deben intervenir sobre determinado espacio o grupo. La aplicación tomará en cuenta las distintas restricciones que cada profesional tiene, buscando evitar posibles superposiciones, ahorrar tiempo y tratar de lograr satisfacer lo más cercanamente posible los objetivos deseados.

**IMPORTANTE:**
Horarios está programado en Django 1.8, si no lo tienes instalado [haz click aquí](https://www.djangoproject.com/download/ "Descargar Django").

###*Configurar la aplicación para su uso:*
#####Una vez clonado el proyecto seguir estos pasos:
* Renombrar el archivo `horarios/settings.base.py` a `horarios/settings.py`.
* Crear la base de datos.
* En su interior realizar los cambios necesarios a la configuración de la base de datos.
* Situarse en el directorio raíz del proyecto.
* Realizar las migraciones del proyecto: `python manage.py makemigrations`.
* Migrar la base de datos: `python manage.py migrate`.
* Iniciar el servidor: `python manage.py runserver 0.0.0.0:8000`.
* Ir a [http://localhost:8000/](http://localhost:8000/).

Y listo!
