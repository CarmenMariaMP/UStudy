from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse
from django.conf import settings
from app.models import *
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
        

        usuarioActual = request.user.usuario

        cursosUsuario = Curso.objects.all().filter(propietario=usuarioActual).order_by('nombre')

        dicc= dict()

        for curso in cursosUsuario:
            archivos = Archivo.objects.all().filter(curso = curso)
            valoraciones = Valoracion.objects.all().filter(curso=curso)
            puntos = 0
            for valoracion in valoraciones:
                puntos += valoracion.puntuacion
            
            if len(valoraciones)>0:
                mediaPuntos=puntos/len(valoraciones)
            else:
                mediaPuntos = "No tiene valoraciones"

            dicc[curso] = (len(archivos),mediaPuntos,len(curso.suscriptores.all()))


        return render(request, "inicio_profesor.html", {'nombre':usuarioActual.nombre, 'dicc':dicc})

    
    else:
        return redirect("/login",{"mensaje_error":True})

def crearcurso(request):
    return render(request, "crearcurso.html")
  
def curso(request, id):
    es_owner = False
    es_suscriptor = False       
    
    curso = Curso.objects.get(id=id)
    contenido_curso = Archivo.objects.all().filter(curso=curso)
    
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(email_academico=usuario_autenticado)
        form = UploadFileForm(request.POST, request.FILES)
        if curso.propietario == usuario:
            es_owner = True
            if request.method == 'POST':
              if form.is_valid():
                file = request.FILES['file']
                curso = Curso.objects.get(id=id)
                archivo = Archivo.objects.create(nombre=file.name, ruta=file, curso=curso)
                archivo.save()
              else:
                form = UploadFileForm()
              
        elif usuario in curso.suscriptores.all():
            es_suscriptor = True
        
            
        return render(request, "curso.html", {"id": id, "es_owner": es_owner, "es_suscriptor": es_suscriptor, "curso":curso ,"contenido_curso": contenido_curso, "form":form})
   
    else:
       return render(request, 'inicio.html')     
  
def miscursos(request):

    if request.user.is_authenticated:
        user1 = request.user.usuario
        cursos = user1.Suscriptores
        

        cursosAlumno = list()

        for curso in cursos.all():
                cursosAlumno.append(curso)

        return render(request, "miscursos.html",{'cursos':cursosAlumno})
    
    else:
        return redirect("/login",{"mensaje_error":True})

def cursosdisponibles(request):
    if request.user.is_authenticated:
        cursos_todos = Curso.objects.order_by('nombre')
        cursos=[]
        for curso in cursos_todos:
            suscriptores = curso.suscriptores.all()
            if (curso.propietario != request.user.usuario):
                if (request.user.usuario not in suscriptores):
                    cursos.append(curso)
        return render(request, "cursosdisponibles.html", {'cursos':cursos})
    else:
        return redirect("/login")
     
def ver_archivo(request, id_curso, id_archivo):
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


