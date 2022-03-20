from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.models import Archivo, Usuario,Curso, Valoracion

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
  
def curso(request):
    return render(request, "curso.html")
  
def miscursos(request):
    return render(request, "miscursos.html")

def cursosdisponibles(request):
    return render(request, "cursosdisponibles.html")
