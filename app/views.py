from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.models import Usuario

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
  
def curso(request):
    return render(request, "curso.html")
  
def miscursos(request):
    return render(request, "miscursos.html")

def cursosdisponibles(request):
    return render(request, "cursosdisponibles.html")

def ver_archivo(request, id_curso, id_archivo):
    return render(request, "archivo.html")
