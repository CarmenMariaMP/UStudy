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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
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
    path('suscripcion/', views.suscripcion),
    path('curso/<int:id_curso>/archivo/<int:id_archivo>', views.ver_archivo)
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
