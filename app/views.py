from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse
from django.conf import settings
from app.models import Usuario, Archivo, Curso, Comentario
from .forms import UploadFileForm
import os

# Create your views here.
def inicio(request):
    return render(request, "inicio.html")

def login_user(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        
        usuario_autenticado = authenticate(username=correo, password=contrasena)

        if usuario_autenticado is not None:
            usuario = usuario_autenticado.usuario
            login(request,usuario_autenticado)
            return redirect("/inicio_profesor",{"nombre":usuario.nombre})
        else:
            return render(request,'login.html',{"mensaje_error":True})
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return render(request, "inicio.html")

def inicio_profesor(request):
    if request.user.is_authenticated:
        return render(request, "inicio_profesor.html", {'nombre': request.user.usuario.nombre})
    else:
        return render(request, 'inicio.html')
  
def curso(request, id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            curso = Curso.objects.get(id=id)
            archivo = Archivo.objects.create(nombre=file.name, ruta=file, curso=curso)
            archivo.save()
    else:
        form = UploadFileForm()
        
    archivos = Archivo.objects.filter(curso=id)
    return render(request, "curso.html", {'form': form, 'archivos': archivos})
  
def miscursos(request):
    return render(request, "miscursos.html")

def cursosdisponibles(request):
    return render(request, "cursosdisponibles.html")
     
def ver_archivo(request, id_curso, id_archivo):
    # TODO coger comentarios
    acceso = False
    curso = Curso.objects.get(id=id_curso)
    contenido_curso = Archivo.objects.all().filter(curso=curso)
    comentarios = Comentario.objects.all().filter(archivo=id_archivo)
    archivo = Archivo.objects.get(id=id_archivo)
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(email_academico=usuario_autenticado)
        if (curso.propietario == usuario) or (usuario in curso.suscriptores.all()):
            acceso = True
        return render(request, "archivo.html", {'pdf':archivo.ruta ,'curso': curso, 'archivo': archivo, 'contenido_curso': contenido_curso, 'acceso': acceso, 'comentarios': comentarios})
    else:
        return render(request, 'inicio.html')
