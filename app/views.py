from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def inicio(request):
    return render(request, "inicio.html")

def login(request):
    return render(request, "login.html")

def inicio_profesor(request):
    return render(request, "inicio_profesor.html")
  
def curso(request):
    return render(request, "curso.html")
  
def miscursos(request):
    return render(request, "miscursos.html")

def cursosdisponibles(request):
    return render(request, "cursosdisponibles.html")
