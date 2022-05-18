from django.contrib import admin
from app.models import Asignatura,Archivo,Curso,Comentario,Notificacion, Resenya, TicketDescarga,Valoracion,Usuario,Reporte, RetiradaDinero


# Register your models here.
admin.site.register(Asignatura)
admin.site.register(Usuario)
admin.site.register(Curso)
admin.site.register(Archivo)
admin.site.register(Comentario)
admin.site.register(Notificacion)
admin.site.register(Valoracion)
admin.site.register(Reporte)
admin.site.register(TicketDescarga)
admin.site.register(RetiradaDinero)
admin.site.register(Resenya)
