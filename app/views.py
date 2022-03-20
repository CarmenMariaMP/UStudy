from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.models import Curso, Usuario

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

    cursos = Curso.objects.all().order_by("nombre")

    cursosAlumno = list()

    for curso in cursos:
        suscriptores = curso.suscriptores.all()
        if request.user.usuario in suscriptores:
            cursosAlumno.append(curso)

    return render(request, "miscursos.html",{'cursos':cursosAlumno})

def cursosdisponibles(request):
    return render(request, "cursosdisponibles.html")
