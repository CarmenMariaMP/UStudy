from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def inicio(request):
    return render(request, "inicio.html")

def login(request):
    return render(request, "login.html")
  
def curso(request):
    return render(request, "curso.html")

def crearcurso(request):
    return render(request, "crearcurso.html")