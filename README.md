*Horarios*
========

***Práctica Profesional/Trabajo Final Integrador 2015 - UDC***

Es una aplicación que permite la organización de horarios y la asignación de los mismos a profesionales que deben intervenir sobre determinado espacio o grupo. La aplicación tomará en cuenta las distintas restricciones que cada profesional tiene, buscando evitar posibles superposiciones, ahorrar tiempo y tratar de lograr satisfacer lo más cercanamente posible los objetivos deseados.

**IMPORTANTE:**
Horarios está programado en Django, si no lo tienes instalado haz click [aquí](https://www.djangoproject.com/download/ "Descargar Django").

###*Configurar la aplicación para su uso:*
#####Una vez clonado el proyecto seguir estos pasos:
* Crear la base de datos.
* Renombrar el archivo `horarios/settings.base.py` a `horarios/settings.py`. En su interior realizar los cambios de acuerdo a tu configuración.
* Situarse en el directorio raíz del proyecto.
* Realizar las migraciones del proyecto: `python manage.py makemigrations`.
* Migrar la base de datos: `python manage.py migrate`.
* Iniciar el servidor: `python manage.py runserver 0.0.0.0:8000`.
* Ir a [http://localhost:8000/](http://localhost:8000/).

Y listo!
