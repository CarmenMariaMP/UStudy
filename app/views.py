from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.models import Usuario
from app.models import Curso

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
    print(request.user)
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