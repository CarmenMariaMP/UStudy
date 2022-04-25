"""ustudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
#from django.conf.urls import url

urlpatterns = [
    #url(r'^archivos/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    #url(r'^/static(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', views.inicio),
    path('admin/', admin.site.urls),
    path('crearcurso/', views.crearcurso),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('inicio_profesor/', views.inicio_profesor),
    path('curso/<int:id>', views.curso),
    path('miscursos/', views.miscursos),
    path('cursosdisponibles/', views.cursosdisponibles),
    path('subir_contenido/', views.subir_contenido),
    path('suscripcion/<int:id>', views.suscripcion),
    path('pago/',views.pago),
    path('comprobacion_pago', views.comprobacion_pago),
    path('curso/<int:id_curso>/archivo/<int:id_archivo>', views.ver_archivo),
    path('valorar_curso/', views.valorar_curso),
    path('curso/<int:id_curso>/<int:id_archivo>', views.borrar_archivo),
    path('registro/', views.registro_usuario),
    path('actualizar_perfil/', views.actualizar_usuario),
    path('curso/<int:id_curso>/archivo/<int:id_archivo>/reporte/<int:id_reporte>',
         views.eliminar_reporte),
    path('curso/<int:id_curso>/archivo/<int:id_archivo>/comentario/<int:id_comentario>',
         views.eliminar_comentario),
    path('perfil/', views.perfil_usuario),
    path('borrar_foto/', views.borrar_foto),
    path('dashboard/', views.dashboard_users),
    path("editarcurso/<int:id_curso>" , views.editar_curso),
    path('sobre_nosotros/', views.sobre_nosotros),
    path('terminos/', views.terminos),
    path('privacidad/', views.privacidad),
    path("notificacion/eliminar/<int:id_notificacion>" , views.eliminar_notificacion),
    path('correo/',views.envio_correo),
    path('informacion_transferencia/',views.informacion_transferencia),
]
#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = views.error_404
handler403 = views.error_403
handler500 = views.error_500
