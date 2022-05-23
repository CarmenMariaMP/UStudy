from django.core.files.storage import default_storage, DefaultStorage, FileSystemStorage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from app import paypal
from app.forms import MonederoForm, ResenyaForm, RetiradaDineroForm, UsuarioForm, CursoForm, ReporteForm, UploadFileForm, CursoEditForm, ActualizarUsuarioForm, ComentarioForm, ResponderComentarioForm, ResponderComentarioForm2
from app.models import Resenya, Usuario, Curso, Archivo, Comentario, Valoracion, Reporte, User, Notificacion, TicketDescarga, RetiradaDinero
from app.paypal import GetOrder
import json
import os
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
from decouple import config
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import mimetypes

from pathlib import Path


from django.core.paginator import Paginator

import smtplib
from email.message import EmailMessage


def envio_correo(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RetiradaDineroForm(request.POST)
            if form.is_valid():
                usuarioActual = request.user.usuario
                paypal = request.POST['paypal']
                confirmar_paypal = request.POST['confirmar_paypal']
                dinero = request.POST['dinero']

                if(paypal != confirmar_paypal):
                    form.add_error("confirmar_paypal",
                                   "Las cuentas no coinciden")
                    return render(request, 'correo.html', {"form": form})

                if(Decimal(dinero) > usuarioActual.dinero):
                    form.add_error("dinero",
                                   "No dispone de esa cantidad en el monedero")
                    return render(request, 'correo.html', {"form": form})

                try:
                    retirada = RetiradaDinero(email=paypal,dinero=Decimal(dinero))
                    retirada.full_clean()
                    retirada.save()

                    usuarioActual.dinero -= Decimal(dinero)
                    usuarioActual.save()
                    
                    email_host_user = config('EMAIL_HOST_USER')
                    email_host_password = config('EMAIL_HOST_PASSWORD')
                    smtp_server = config('EMAIL_HOST')
                    msg = EmailMessage()
                    msg['Subject'] = "Retirada Dinero"
                    msg['From'] = email_host_user
                    msg['To'] = email_host_user
                    msg.set_content("La cuenta de correo del usuario que desea sacar el dinero es " + request.user.usuario.email + ". La cuenta de paypal a la que realizar la transferencia es " + paypal + ". El dinero que desea sacar es " + dinero + "€.")
                    
        
                    server = smtplib.SMTP(smtp_server)
                    server.starttls()
                    server.login(email_host_user, email_host_password)
                    server.send_message(msg)
                    server.quit()

                    return redirect('/informacion_transferencia')
                except Exception:
                    
                    return redirect('/informacion_error_transferencia') 
            else:
                return render(request, 'correo.html', {"form": form})

        else:
            form = RetiradaDineroForm()

            return render(request, "correo.html", {"form": form})
    else:
        return redirect("/login")


def buscar_curso(request):

    busqueda = request.GET.get('q')
    cursos_todos = Curso.objects.filter(asignatura__nombre__icontains=busqueda)
    cursos = []
    usuario_actual = request.user.usuario
    for curso in cursos_todos:
        suscriptores = curso.suscriptores.all()
        if (curso.propietario != usuario_actual):
            if (usuario_actual not in suscriptores and usuario_actual.titulacion == curso.asignatura.titulacion):
                valoracion = get_valoracion(curso)
                cursos.append((curso, valoracion))
    page_obj = pagination(request, cursos, 9)
    return render(request, "cursosdisponibles.html", {'page_obj': page_obj})




def informacion_transferencia(request):

    if request.user.is_authenticated:

        return render(request, 'informacion_transferencia.html')

    else:
        return redirect("/login")

def informacion_error_transferencia(request):

    if request.user.is_authenticated:

        return render(request, 'informacion_error_transferencia.html')

    else:
        return redirect("/login")


def pagination(request, productos, num):
    paginator = Paginator(productos, num)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_valoracion(curso):
    valoraciones = Valoracion.objects.all().filter(curso=curso)
    puntos = 0
    mediaPuntos = "No tiene valoraciones"
    for valoracion in valoraciones:
        puntos += valoracion.puntuacion
    if len(valoraciones) > 0:
        mediaPuntos = round(puntos/len(valoraciones), 2)
    return mediaPuntos

# Create your views here.


def inicio(request):
    if not request.user.is_authenticated:
        return render(request, "inicio.html")
    else:
        user1 = request.user.usuario
        cursos = user1.Suscriptores

        cursosAlumno = list()

        for curso in cursos.all():
            valoracion = get_valoracion(curso)
            cursosAlumno.append((curso, valoracion))

        page_obj = pagination(request, cursosAlumno, 9)
        return render(request, "miscursos.html", {'page_obj': page_obj})


def pago(request):
    if request.user.is_authenticated:
        # si es una consulta post (enviando el formulario)
        if request.method == 'POST':
            form = MonederoForm(request.POST)
            if form.is_valid():
                dinero = request.POST['dinero']
                client_id = config('PAYPAL_CLIENT_ID')

                return render(request, "pasarela_pago.html", context={"client_id": client_id, "dinero": dinero, "username": request.user.username})
            else:
                return render(request, 'pasarela_pago.html', {"form": form})

        else:
            form = MonederoForm()

            return render(request, "pasarela_pago.html", {"form": form})
    else:
        return redirect("/login")


def comprobacion_pago(request):
    if request.user.is_authenticated:

        data = json.loads(request.body)

        if data:

            order_id = data['orderID']
            detalle = GetOrder().get_order(order_id)
            detalle_precio = float(
                detalle.result.purchase_units[0].amount.value)

            usuarioActual = request.user.usuario

            usuarioActual.dinero = float(usuarioActual.dinero) + detalle_precio
            usuarioActual.save()
            data = {
                "mensaje": "Se ha añadido el dinero correctamente"
            }
            return JsonResponse(data)
        else:
            data = {
                "mensaje": "Error =("
            }
            return JsonResponse(data)

    else:
        return redirect("/login")


def suscripcion(request, id):
    if request.user.is_authenticated:

        usuario = Usuario.objects.get(django_user=request.user)
        curso_var = Curso.objects.get(pk=id)
        if usuario.titulacion != curso_var.asignatura.titulacion or curso_var.propietario == usuario:
            return cursosdisponibles(request, mensaje_error=True, mensaje="No puedes suscribirte a este curso")

        if usuario in curso_var.suscriptores.all():
            return cursosdisponibles(request, mensaje_error=True, mensaje="Ya estás suscrito al curso")

        if usuario.dinero < Decimal(12.00):
            return cursosdisponibles(request, mensaje_error=True, mensaje="No tienes dinero suficiente")

        else:
            curso_var.suscriptores.add(usuario)
            usuario.dinero -= Decimal(12.00)
            profesor = curso_var.propietario
            profesor.dinero += Decimal(8.00)
            curso_var.save()
            usuario.save()
            profesor.save()

            referencia = '/curso/' + str(curso_var.id)
            notificacion = Notificacion(referencia=referencia, usuario=profesor,
                                        tipo="NUEVO_ALUMNO", curso=curso_var, visto=False, alumno=usuario)
            notificacion.save()
            suscrito = "Se ha suscrito correctamente al curso"
            return render(request, 'cursosdisponibles.html', {'curso': curso_var, 'suscrito': suscrito})

    else:
        return redirect("/login")

def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            usuario = request.POST['username']
            contrasena = request.POST['contrasena']

            usuario_autenticado = authenticate(
                username=usuario, password=contrasena)

            if usuario_autenticado is not None:
                usuario = usuario_autenticado.usuario
                login(request, usuario_autenticado)
                return redirect("/miscursos", {"nombre": usuario})
            else:
                return render(request, 'login.html', {"mensaje_error": True})
        return render(request, "login.html")
    else:
        user1 = request.user.usuario
        cursos = user1.Suscriptores

        cursosAlumno = list()

        for curso in cursos.all():
            valoracion = get_valoracion(curso)
            cursosAlumno.append((curso, valoracion))

        page_obj = pagination(request, cursosAlumno, 9)
        return render(request, "miscursos.html", {'page_obj': page_obj})


def logout_user(request):
    logout(request)
    return render(request, "inicio.html")


def borrar_foto(request):
    if request.user.is_authenticated:
        usuarioActual = request.user.usuario
        usuarioActual.foto.delete(save=True)
        try:
            os.remove("app/static/files/" +
                    request.user.username + ".jpg")
        except:
            pass
        return redirect("/actualizar_perfil")
    else:
        return redirect("/login")


def perfil_usuario(request, username):
    owner_perfil = False
    if request.user.is_authenticated:
        usuario_actual = Usuario.objects.filter(django_user=request.user).prefetch_related('Suscriptores').get()
        cursos_suscritos = usuario_actual.Suscriptores.all()

        user_perfil = User.objects.get(username=username)
        usuario_perfil = user_perfil.usuario
        if request.user == user_perfil:
            owner_perfil = True

        nombre = usuario_perfil.nombre+' '+usuario_perfil.apellidos
        titulacion = usuario_perfil.titulacion
        dinero = usuario_perfil.dinero
        descripcion = usuario_perfil.descripcion

        try:
            foto = usuario_perfil.foto.url
        except:
            foto = "None"

        url = foto.replace("app/static/", "")


        cursosUsuario = Curso.objects.all().filter(
            propietario=usuario_perfil)
        valoracion_total= 0
        numero_valoraciones = 0
        for curso in cursosUsuario:
            valoraciones = Valoracion.objects.all().filter(curso=curso)
            puntos = 0
            for valoracion in valoraciones:
                puntos += valoracion.puntuacion

            if len(valoraciones) > 0:
                valoracion_total += puntos
                numero_valoraciones += len(valoraciones)
        if(numero_valoraciones!=0):
            valoracion_media = round(valoracion_total/numero_valoraciones, 2)
        else:   
            valoracion_media = 0
            
        notificaciones = Notificacion.objects.all().filter(
            usuario=usuario_perfil).order_by('-fecha')
        valoracion_media_redondeada = round(valoracion_media)
        
        return render(request, "perfil.html", { "cursos_suscritos": cursos_suscritos, "nombre": nombre, "titulacion": titulacion,"cursos": cursosUsuario,"descripcion":descripcion,
                                               "dinero": dinero, "valoracion_media": valoracion_media, "foto": url, "notificaciones": notificaciones, "owner": owner_perfil, 
                                               "rango_r": range(valoracion_media_redondeada), "rango_sr": range(5-valoracion_media_redondeada)})

    else:
        return redirect("/login", {"mensaje_error": True})


def inicio_profesor(request):
    if request.user.is_authenticated:

        usuarioActual = request.user.usuario

        cursosUsuario = Curso.objects.all().filter(
            propietario=usuarioActual).order_by('nombre')

        dicc = dict()
        val = 0
        ac = 0
        acc_sum = 0

        for curso in cursosUsuario:
            archivos = Archivo.objects.all().filter(curso=curso)
            valoraciones = Valoracion.objects.all().filter(curso=curso)
            puntos = 0

            for valoracion in valoraciones:
                puntos += valoracion.puntuacion

            if len(valoraciones) > 0:
                mediaPuntos = puntos/len(valoraciones)
                acc_sum += mediaPuntos
                ac += 1

            else:
                mediaPuntos = "No tiene valoraciones"

            dicc[curso] = (len(archivos), mediaPuntos,
                           len(curso.suscriptores.all()))

            if (ac > 0):
                val = acc_sum / ac

        lista_pagination = [(x, dicc[x]) for x in dicc]
        page_obj = pagination(request, lista_pagination, 9)

        return render(request, "inicio_profesor.html", {'nombre': usuarioActual.nombre, 'val': val, 'ac': ac, 'page_obj': page_obj})

    else:
        return redirect("/login", {"mensaje_error": True})


def crearcurso(request):

    # si el usuario está autenticado
    if request.user.is_authenticated:
        # si es una consulta post (enviando el formulario)
        if request.method == 'POST':
            form = CursoForm(request.user, request.POST)
            if form.is_valid():
                curso = form.save(commit=False)
                curso.fecha_publicacion = datetime.datetime.now()
                curso.propietario = Usuario.objects.get(
                    django_user=request.user)
                curso.save()
                return redirect('/inicio_profesor')
            else:
                return render(request, 'crearcurso.html', {"form": form})

        else:  # si es una consulta get vamos a la vista con el formulario vacio
            form = CursoForm(user=request.user)

            return render(request, "crearcurso.html", {"form": form})
    else:
        return render(request, 'inicio.html')


def registro_usuario(request):

    # si el usuario está autenticado
    # si es una consulta post (enviando el formulario)
    if request.user.is_authenticated:
        return redirect("/miscursos")

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario_form = form.cleaned_data
            password = usuario_form['password']
            confirm_password = usuario_form['confirm_password']
            usename = usuario_form['username']
            name = usuario_form['name']
            surname = usuario_form['surname']
            email = usuario_form['email']
            email_academico = usuario_form['email_academico']
            titulacion = usuario_form['titulacion']
            descripcion = usuario_form['descripcion']
            dinero = 0.0
            terminos = usuario_form['terminos']
            privacidad = usuario_form['privacidad']
            # Comprobación contraseña
            if(password != confirm_password):
                form.add_error("confirm_password",
                               "Las contraseñas no coinciden")
                return render(request, 'registro.html', {"mensaje_error": True, "form": form})

            user_instancia = User(
                username=usename, email=email, password=password)
            usuario_instancia = Usuario(
                nombre=name, apellidos=surname, email=email, email_academico=email_academico, titulacion=titulacion, descripcion=descripcion, dinero=dinero)

            # validación userjango
            try:
                user_instancia.full_clean()
                user_django = User.objects.create_user(
                    username=usename, email=email, password=password)
                user_django.save()

            except ValidationError as e:
                for i in e.error_dict:
                    form.add_error(i, e.error_dict[i])

                return render(request, 'registro.html', {"mensaje_error": True, "form": form})

            # validación Usuario Ustudy
            try:
                usuario_instancia.django_user = user_django

                usuario_instancia.full_clean()

                usuario_instancia.save()

            except ValidationError as e:
                user_django.delete()
                for i in e.error_dict:
                    form.add_error(i, e.error_dict[i])

                return render(request, 'registro.html', {"mensaje_error": True, "form": form})

            return redirect("/login")
        else:
            return render(request, 'registro.html', {"form": form})

    else:  # si es una consulta get vamos a la vista con el formulario vacio
        form = UsuarioForm()

        return render(request, "registro.html", {"form": form})


def actualizar_usuario(request):

    # si el usuario está autenticado
    # si es una consulta post (enviando el formulario)
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = ActualizarUsuarioForm(request.POST, request.FILES)
            try:
                kkk = request.user.usuario.foto.url
            except:
                kkk = "None"

            url = kkk.replace("app/static/", "")
            if form.is_valid():
                usuario_form = form.cleaned_data
                contrasena = usuario_form['contrasena']
                confirmar_contrasena = usuario_form['confirmar_contrasena']
                username = usuario_form['username']
                nombre = usuario_form['nombre']
                apellidos = usuario_form['apellidos']
                email = usuario_form['email']
                email_academico = Usuario.objects.get(
                    django_user=request.user).email_academico
                titulacion = usuario_form['titulacion']
                descripcion = usuario_form['descripcion']
                foto = usuario_form['foto']
                dinero = Usuario.objects.get(django_user=request.user).dinero

                # Comprobación contraseña
                if(contrasena != confirmar_contrasena):
                    form.add_error("confirmar_contrasena",
                                   "Las contraseñas no coinciden")
                    return render(request, 'actualizar.html', {"mensaje_error": True, "form": form, 'url': url})
                if foto != None:
                    if not any(foto.name[-4:] in item for item in ['.jpg', '.png', 'jpeg']):
                        form.add_error(
                            "foto", "Formato de imagen no válido, solo se permiten .jpg, .png y .jpeg")
                        return render(request, 'actualizar.html', {"mensaje_error": True, "form": form, 'url': url})

                user_instancia = User(
                    username=request.user.username, password=contrasena)
                usuario_instancia = Usuario(
                    nombre=nombre, apellidos=apellidos, email=email, email_academico=email_academico, titulacion=titulacion, descripcion=descripcion, dinero=dinero, foto=foto)

                # validación usuario
                try:
                    usuario_instancia.full_clean(
                        exclude=['django_user', 'email', 'email_academico'])
                    if(request.user.usuario.email != email and Usuario.objects.filter(email=email).exists()):
                        form.add_error("email", "Este email ya existe")
                        return render(request, 'actualizar.html', {"mensaje_error": True, "form": form, "url": url})

                except ValidationError as e:
                    for i in e.error_dict:
                        form.add_error(i, e.error_dict[i])

                    return render(request, 'actualizar.html', {"mensaje_error": True, "form": form, "url": url})

                try:
                    comprobacion = 0
                    # validación usuario django
                    if(user_instancia.username != username and User.objects.filter(username=username).exists()):
                        form.add_error("username", "Este username ya existe")
                        return render(request, 'actualizar.html', {"mensaje_error": True, "form": form, "url": url})

                    elif(user_instancia.username != username and not User.objects.filter(username=username).exists()):
                        request.user.username = username
                        comprobacion += 1

                    if(contrasena != "" and confirmar_contrasena != ""):
                        request.user.set_password(contrasena)
                        comprobacion += 1

                    if comprobacion > 0:
                        request.user.save()

                except ValidationError as e:
                    for i in e.error_dict:
                        form.add_error(i, e.error_dict[i])

                    return render(request, 'actualizar.html', {"mensaje_error": True, "form": form, "url": url})

                check = False
                only_username = False
                if(foto != None and os.path.exists('app/static/files/'+user_instancia.username+'.jpg')):
                    os.remove("app/static/files/" +
                              user_instancia.username + ".jpg")
                    foto.name = username + ".jpg"
                    # save foto in static/archivos
                    BASE_DIR = Path(__file__).resolve().parent.parent
                    path = FileSystemStorage(location=os.path.join(BASE_DIR, 'app/static/files'), base_url='/app/static/files').save(
                        foto.name, ContentFile(foto.read()))
                    os.path.join(settings.MEDIA_ROOT, path)
                    check = True

                elif (foto != None and not os.path.exists('app/static/files/'+request.user.username+'.jpg')):
                    foto.name = username + ".jpg"
                    # save foto in static/archivos
                    BASE_DIR = Path(__file__).resolve().parent.parent
                    path = FileSystemStorage(location=os.path.join(BASE_DIR, 'app/static/files'), base_url='/app/static/files').save(
                        foto.name, ContentFile(foto.read()))
                    os.path.join(settings.MEDIA_ROOT, path)
                    check = True

                elif (foto == None and user_instancia.username != username and os.path.exists('app/static/files/'+user_instancia.username+'.jpg')):
                    os.rename("app/static/files/" +
                              user_instancia.username + ".jpg", "app/static/files/" + username + ".jpg")
                    only_username = True

                # actualizar usuario Ustudy
                try:
                    if(check):
                        Usuario.objects.filter(django_user=request.user).update(
                            nombre=nombre, apellidos=apellidos, email=email, email_academico=email_academico, titulacion=titulacion, descripcion=descripcion, dinero=dinero, foto=foto)
                    elif(only_username):
                        Usuario.objects.filter(django_user=request.user).update(
                            nombre=nombre, apellidos=apellidos, email=email, email_academico=email_academico, titulacion=titulacion, descripcion=descripcion, dinero=dinero,
                            foto=username+'.jpg')
                    else:
                        Usuario.objects.filter(django_user=request.user).update(
                            nombre=nombre, apellidos=apellidos, email=email, email_academico=email_academico, titulacion=titulacion, descripcion=descripcion, dinero=dinero, foto=Usuario.objects.get(django_user=request.user).foto)

                except ValidationError as e:
                    for i in e.error_dict:
                        form.add_error(i, e.error_dict[i])

                    return render(request, 'actualizar.html', {"mensaje_error": True, "form": form, "url": url})

                return redirect('/login')
            else:
                return render(request, 'actualizar.html', {"form": form, "url": url})

        else:  # si es una consulta get vamos a la vista con el formulario vacio
            usuario = Usuario.objects.get(django_user=request.user)
            try:
                foto = request.user.usuario.foto.url
            except:
                foto = "None"

            url = foto.replace("app/static/", "")

            form = ActualizarUsuarioForm(initial={
                'username': usuario.django_user.username,
                'nombre': usuario.nombre,
                'apellidos': usuario.apellidos,
                'email': usuario.email,
                'email_academico': usuario.email_academico,
                'titulacion': usuario.titulacion,
                'descripcion': usuario.descripcion,
                'foto': usuario.foto
            })

            return render(request, "actualizar.html", {"form": form, "url": url})
    else:
        return render(request, 'inicio.html')


def editar_curso(request, id_curso):
    if request.user.is_authenticated:
        curso = Curso.objects.get(id=id_curso)
        if request.user.usuario == curso.propietario:
            if request.method == 'POST':
                form = CursoEditForm(
                    request.user, request.POST, instance=curso)
                if form.is_valid():
                    curso_form = form.cleaned_data
                    nombre = curso_form['nombre']
                    descripcion = curso_form['descripcion']
                    asignatura = curso_form['asignatura']
                    curso.nombre = nombre
                    curso.descripcion = descripcion
                    curso.asignatura = asignatura
                    curso.save()
                    return redirect("/inicio_profesor")
                else:
                    return render(request, 'editarcurso.html', {"form": form})
            else:
                form = CursoEditForm(request.user, instance=curso)
                return render(request, "editarcurso.html", {"form": form, "curso": curso})
        else:
            return redirect("/miscursos")
    else:
        return redirect("/login")


def curso(request, id, suscrito=False):
    es_owner = False
    es_suscriptor = False

    valoracionCurso = 0

    curso = Curso.objects.get(id=id)

    contenido_curso = Archivo.objects.all().filter(curso=curso).order_by('fecha_publicacion')

    resenyas = Resenya.objects.all().filter(
        curso=curso).order_by('-fecha')


    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        if usuario.titulacion != curso.asignatura.titulacion and usuario not in curso.suscriptores.all() and usuario != curso.propietario:
            return redirect('/cursosdisponibles')
        form = UploadFileForm(request.POST, request.FILES)
        formUpdate = UploadFileForm(request.POST, request.FILES)
        excede_tamano = False
        excede_mensaje = ""
        valoracionCurso = get_valoracion(curso)
        formResenya = ResenyaForm()
        valoracionUsuario = "No has valorado este curso"
        nombre_archivo_unico = True
        if curso.propietario == usuario:
            es_owner = True
            if request.method == 'POST':
                if form.is_valid():
                    file = request.FILES['file']
                    curso = Curso.objects.get(id=id)
                    archivo_instancia = Archivo(
                        nombre=file.name, ruta=file, curso=curso)
                    if file.name in curso.archivos.values_list('nombre', flat=True):
                        nombre_archivo_unico = False
                    else:
                        try:
                            archivo_instancia.full_clean()
                            archivo_instancia.save()
                        except ValidationError as e:
                            excede_tamano = True
                            excede_mensaje = e.message_dict['ruta'][0]
                else:
                    form = UploadFileForm()
                    formUpdate = UploadFileForm()
                
        elif usuario in curso.suscriptores.all():
            es_suscriptor = True
            try:
                valoracionUsuario = Valoracion.objects.get(
                    curso=curso, usuario=usuario).puntuacion
            except:
                pass
            if request.method == 'POST':
                if request.POST['action'] == 'Publicar reseña':
                    formResenya = ResenyaForm(request.POST)
                    if formResenya.is_valid():
                        resenyaForm = formResenya.cleaned_data
                        descripcion = resenyaForm['descripcion']
                        resenya_instancia = Resenya(descripcion=descripcion, fecha=datetime.datetime.now(), curso=curso, usuario=usuario)
                        try:
                            resenya_instancia.full_clean()
                            resenya_instancia.save()
                        except ValidationError as e:
                            print(e)
                        referencia = '/curso/' + \
                        str(id)
                        notificacion = Notificacion(referencia=referencia, usuario=curso.propietario, tipo="NUEVA RESEÑA", curso=curso, visto=False,
                                                alumno=usuario, descripcion=descripcion)
                        notificacion.save()
                        return redirect('/curso/'+str(id))
                    else:
                        return render(request, "curso.html", {"id": id, "es_owner": es_owner, "error_resenya": True, "es_suscriptor": es_suscriptor, "curso": curso, "contenido_curso": contenido_curso, "form": UploadFileForm(), "formResenya":ResenyaForm(), "excede_tamano": excede_tamano, "excede_mensaje": excede_mensaje, "valoracionCurso": valoracionCurso, "valoracionUsuario": valoracionUsuario, "suscrito": suscrito,"nombre_archivo_unico": nombre_archivo_unico, "formUpdate": UploadFileForm(), "resenyas":resenyas})

        return render(request, "curso.html", {"id": id, "es_owner": es_owner, "es_suscriptor": es_suscriptor, "curso": curso, "contenido_curso": contenido_curso, "form": form, "formResenya":formResenya, "excede_tamano": excede_tamano, "excede_mensaje": excede_mensaje, "valoracionCurso": valoracionCurso, "valoracionUsuario": valoracionUsuario, "suscrito": suscrito,"nombre_archivo_unico": nombre_archivo_unico, "formUpdate": formUpdate, "resenyas":resenyas})

    else:
        return render(request, 'inicio.html')


def valorar_curso(request):
    if request.method == "POST":
        el_id = request.POST.get('id')
        val = request.POST.get('valoracion')

        curso = Curso.objects.get(id=el_id)
        usuario = Usuario.objects.get(django_user=request.user)

        if Valoracion.objects.filter(curso=curso, usuario=usuario).count() == 0:
            valoracion = Valoracion()
            valoracion.puntuacion = val
            valoracion.curso = curso
            valoracion.usuario = usuario
            valoracion.save()
        else:
            valoracion = Valoracion.objects.get(curso=curso, usuario=usuario)
            valoracion.puntuacion = val
            valoracion.save()

        return JsonResponse({'succes': 'true', 'score': val}, safe=False)
    return JsonResponse({'succes': 'false'})


def borrar_archivo(request, id_curso, id_archivo):
    curso = Curso.objects.get(id=id_curso)
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        if (curso.propietario == usuario):
            numero_archivos_curso = curso.archivos.count()
            if(numero_archivos_curso < 4):
                messages.info(request, 'Mínimo de archivos posible - Debes tener al menos 3 archivos subidos a un curso para poder borrar uno, prueba a actualizarlo!')
                return HttpResponseRedirect('/curso/' + str(id_curso))
            archivo = Archivo.objects.get(id=id_archivo)
            archivo.delete()
            nombre = archivo.nombre.replace(" ", "_")
            try:   
                os.remove("files/" +
                    str(curso.id) +"/" +  nombre)
                print("Success")
            except:
                print("Failed")
                pass
    return redirect('/curso/'+str(id_curso))


def miscursos(request):

    if request.user.is_authenticated:
        user1 = request.user.usuario
        cursos = user1.Suscriptores
        cursosAlumno = list()

        for curso in cursos.all():
            valoracion = get_valoracion(curso)
            cursosAlumno.append((curso, valoracion))

        page_obj = pagination(request, cursosAlumno, 9)

        return render(request, "miscursos.html", {'page_obj': page_obj})

    else:
        return redirect("/login", {"mensaje_error": True})


def cursosdisponibles(request, mensaje_error=False, mensaje=''):
    if request.user.is_authenticated:
        cursos_todos = Curso.objects.order_by('nombre')
        cursos = []
        numero_archivos = []
        usuario_actual = request.user.usuario
        for curso in cursos_todos:
            suscriptores = curso.suscriptores.all()
            archivos = len(curso.archivos.all())
            numero_archivos.append(archivos)
            if (curso.propietario != usuario_actual):
                if (usuario_actual not in suscriptores and usuario_actual.titulacion == curso.asignatura.titulacion):
                    valoracion = get_valoracion(curso)
                    cursos.append((curso, valoracion))
        page_obj = pagination(request, cursos, 9)
        page_obj_archivos = zip(page_obj,numero_archivos)
        return render(request, "cursosdisponibles.html", {'page_obj': page_obj,"page_obj_archivos":page_obj_archivos,"mensaje_error": mensaje_error, "mensaje": mensaje})
    else:
        return redirect("/login")


def ver_archivo(request, id_curso, id_archivo):
    acceso = False
    es_owner = False
    es_plagio = False
    es_error = False
    curso = Curso.objects.get(id=id_curso)
    contenido_curso = Archivo.objects.all().filter(curso=curso)
    comentarios = Comentario.objects.all().filter(
        archivo=id_archivo, responde_a=None).order_by('-fecha')
    respuestas = Comentario.objects.all().filter(
        archivo=id_archivo, responde_a__isnull=False)
    respuestasDict = {}
    for respuesta in respuestas:
        if respuesta.responde_a.id not in respuestasDict.keys():
            respuestasDict[respuesta.responde_a.id] = [respuesta]
        else:
            respuestasDict[respuesta.responde_a.id].append(respuesta)
    archivo = Archivo.objects.get(id=id_archivo)
    url = archivo.ruta.url.replace("files", "archivos")
    print("URL", url)
    reportes = None
    page_obj = None
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        if (curso.propietario == usuario):
            reportes = Reporte.objects.all().filter(archivo=archivo)
            #page_obj = pagination(request, reportes, 5)
            acceso = True
            es_owner = True
        if (usuario in curso.suscriptores.all()):
            acceso = True

        # si es una consulta post (enviando el formulario)
        if request.method == 'POST':
            if request.POST['action'] == 'Reportar':
                formReporte = ReporteForm(request.POST)
                if formReporte.is_valid():
                    reporteForm = formReporte.cleaned_data
                    descripcion = reporteForm['descripcion']
                    tipo = reporteForm['tipo']
                    reporte_instancia = Reporte(
                        descripcion=descripcion, tipo=tipo, usuario=usuario, archivo=archivo)
                    reporte_instancia.save()
                    referencia = '/curso/' + \
                        str(id_curso)+'/archivo/'+str(id_archivo)
                    notificacion = Notificacion(referencia=referencia, usuario=curso.propietario, tipo="REPORTE", curso=curso, visto=False,
                                                alumno=usuario, descripcion=descripcion)
                    notificacion.save()
                    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))
            elif request.POST['action'] == 'Comentar':
                formComentario = ComentarioForm(request.POST)
                if formComentario.is_valid():
                    comentarioForm = formComentario.cleaned_data
                    texto = comentarioForm['texto']
                    Comentario.objects.create(
                        texto=texto, archivo=archivo, fecha=datetime.datetime.now(), usuario=usuario)
                    referencia = '/curso/' + \
                        str(id_curso)+'/archivo/'+str(id_archivo)
                    notificacion = Notificacion(referencia=referencia, usuario=curso.propietario, tipo="COMENTARIO", curso=curso, visto=False,
                                                alumno=usuario, descripcion=texto)
                    notificacion.save()
                    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))
                else:
                    return render(request, "archivo.html", {'pdf': archivo.ruta, 'curso': curso, 'archivo': archivo, 'contenido_curso': contenido_curso, 'respuestasDict': respuestasDict, 'error': True,
                                                    'acceso': acceso, 'comentarios': comentarios, 'url': url, 'formReporte': ReporteForm(), 'reportes': reportes, 'es_owner': es_owner,
                                                    'usuario': usuario, 'es_plagio': es_plagio, 'es_error': es_error, 'formComentario': ComentarioForm(), 'formRespuesta': ResponderComentarioForm(), 'formRespuesta2': ResponderComentarioForm2()})
                    
            elif request.POST['action'] == 'Responder':
                formRespuesta = ResponderComentarioForm(request.POST)
                if formRespuesta.is_valid():
                    responderForm = formRespuesta.cleaned_data
                    responde_a = responderForm['responde_a']
                    texto = responderForm['texto']
                    Comentario.objects.create(texto=texto, archivo=archivo, fecha=datetime.datetime.now(
                    ), usuario=usuario, responde_a=Comentario.objects.get(id=responde_a))
                    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))
                else:
                    return render(request, "archivo.html", {'pdf': archivo.ruta, 'curso': curso, 'archivo': archivo, 'contenido_curso': contenido_curso, 'respuestasDict': respuestasDict, 'error': True,
                                                    'acceso': acceso, 'comentarios': comentarios, 'url': url, 'formReporte': ReporteForm(), 'reportes': reportes, 'es_owner': es_owner,
                                                    'usuario': usuario, 'es_plagio': es_plagio, 'es_error': es_error, 'formComentario': ComentarioForm(), 'formRespuesta': ResponderComentarioForm(), 'formRespuesta2': ResponderComentarioForm2()})
            elif request.POST['action'] == 'Responder2':
                formRespuesta2 = ResponderComentarioForm2(request.POST)
                if formRespuesta2.is_valid():
                    responderForm = formRespuesta2.cleaned_data
                    usuario_responde_a = responderForm['usuario_responde_a']
                    responde_a = responderForm['responde_a']
                    texto = responderForm['texto']
                    texto = "@"+usuario_responde_a+" "+texto
                    Comentario.objects.create(texto=texto, archivo=archivo, fecha=datetime.datetime.now(
                    ), usuario=usuario, responde_a=Comentario.objects.get(id=responde_a))
                    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))
                else:
                    return render(request, "archivo.html", {'pdf': archivo.ruta, 'curso': curso, 'archivo': archivo, 'contenido_curso': contenido_curso, 'respuestasDict': respuestasDict, 'error': True,
                                                    'acceso': acceso, 'comentarios': comentarios, 'url': url, 'formReporte': ReporteForm(), 'reportes': reportes, 'es_owner': es_owner,
                                                    'usuario': usuario, 'es_plagio': es_plagio, 'es_error': es_error, 'formComentario': ComentarioForm(), 'formRespuesta': ResponderComentarioForm(), 'formRespuesta2': ResponderComentarioForm2()})
        else:
            if acceso:
                print("crear ticket")
                ticket = TicketDescarga(usuario=Usuario.objects.get(
                    django_user=request.user), archivo=archivo)
                print(ticket)
                ticket.save()

            formComentario = ComentarioForm()
            formReporte = ReporteForm()
            formRespuesta = ResponderComentarioForm()
            formRespuesta2 = ResponderComentarioForm2()
            return render(request, "archivo.html", {'pdf': archivo.ruta, 'curso': curso, 'archivo': archivo, 'contenido_curso': contenido_curso, 'respuestasDict': respuestasDict,
                                                    'acceso': acceso, 'comentarios': comentarios, 'url': url, 'formReporte': ReporteForm(), 'reportes': reportes, 'es_owner': es_owner,
                                                    'usuario': usuario, 'es_plagio': es_plagio, 'es_error': es_error, 'formComentario': ComentarioForm(), 'formRespuesta': ResponderComentarioForm(), 'formRespuesta2': ResponderComentarioForm2()})
    else:
        return render(request, 'inicio.html')


def eliminar_comentario(request, id_curso, id_archivo, id_comentario):
    comentario = Comentario.objects.get(id=id_comentario)
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(django_user=request.user)
        if (comentario.usuario == usuario):
            Comentario.objects.filter(id=id_comentario).update(texto='Este comentario ha sido eliminado',
                                                               fecha=comentario.fecha, archivo=comentario.archivo, responde_a=comentario.responde_a, usuario=comentario.usuario)
    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))


def eliminar_reporte(request, id_curso, id_archivo, id_reporte):
    curso = Curso.objects.get(id=id_curso)
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        if (curso.propietario == usuario):
            reporte = Reporte.objects.get(id=id_reporte)
            reporte.delete()
    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))


def eliminar_notificacion(request, id_notificacion):
    notificacion = Notificacion.objects.get(id=id_notificacion)
    if request.user.is_authenticated:
        usuario_autenticado = request.user
        
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        if (notificacion.usuario == usuario):
            Notificacion.objects.filter(id=id_notificacion).update(visto=True)
    return redirect('/perfil/'+str(request.user.username))


def dashboard_users(request):
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        cursos = usuario.Suscriptores
        cursos_suscritos = []
        numero_valoraciones = 0
        num_archivos = 0
        numero_reportes = 0
        num_susriptores = 0
        valoracion_media_global = 0

        for c in cursos.all():
            curso = Curso.objects.get(id=c.id)
            cursos_suscritos.append(curso)

        cursos_propietario = Curso.objects.filter(propietario=usuario)

        for c in cursos_propietario:
            curso = Curso.objects.get(id=c.id)
            valoraciones = Valoracion.objects.all().filter(curso=curso)
            numero_valoraciones += len(valoraciones)
            try:
                valoracion = get_valoracion(curso)
                valoracion_media_global += valoracion
            except:
                valoracion_media_global += 0.0
            num_susriptores += len(curso.suscriptores.all())
            archivos_curso = Archivo.objects.filter(curso=curso)
            num_archivos += len(archivos_curso)
            reportes = list()
            for archivo in archivos_curso:
                reporte = Reporte.objects.all().filter(
                    archivo=Archivo.objects.get(id=archivo.id))
                reportes.append(reporte)
            numero_reportes += len(reportes)

        try:
            valoracion_media_global = round(valoracion_media_global / len(cursos_propietario), 2)
        except:
            valoracion_media_global = 0.0

        return render(request, 'dashboard.html', {'usuario': usuario, 'cursos_suscritos': len(cursos_suscritos),
                                                  'cursos_propietario': len(cursos_propietario), "suscriptores": num_susriptores, 'archivos_subidos': num_archivos,
                                                  'reportes': numero_reportes, 'valoraciones': numero_valoraciones, 'valoracion_media_global': valoracion_media_global})
    return render(request, 'inicio.html')


def subir_contenido(request):
    return render(request, "subir_contenido.html")


def error_404(request, exception):
    context = {"error": "Parece que esta página no existe..."}
    return render(request, 'error.html', context)


def error_403(request, exception):
    context = {"error": "Parece que no tienes acceso a esta página..."}
    return render(request, 'error.html', context)


def error_500(request):
    context = {"error": "Parece que hay un error en el servidor..."}
    return render(request, 'error.html', context)


def servir_archivo(request, id_curso, archivo):
    if request.user.is_authenticated:
        curso = Curso.objects.get(pk=id_curso)
        usuario = Usuario.objects.filter(django_user=request.user)[0]
        if usuario == curso.propietario or usuario in curso.suscriptores.all():
            tickets = TicketDescarga.objects.filter(
                usuario=usuario, archivo=Archivo.objects.filter(curso=id_curso,ruta=str(id_curso)+"/"+str(archivo))[0])
            if len(tickets) > 0:
                filename = "./files/"+str(curso.id)+"/"+archivo
                wrapper = FileWrapper(open(filename, "rb"))
                response = HttpResponse(wrapper, content_type=mimetypes.guess_type(
                    "./files/"+str(curso.id)+"/"+archivo)[0])
                response['Content-Length'] = os.path.getsize(filename)
                tickets[0].delete()
                return response
            else:
                return error_403(request, None)
        else:
            return error_403(request, None)
    else:
        return error_403(request, None)
    
def editar_archivo(request, id_curso, id_archivo):
    curso = Curso.objects.get(id=id_curso)
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        formUpdate = UploadFileForm(request.POST, request.FILES)
        if (curso.propietario == usuario):
            if request.method == 'POST':
                if formUpdate.is_valid():
                    file = request.FILES['file']
                    archivo = Archivo.objects.get(id=id_archivo)
                    fecha = archivo.fecha_publicacion
                    archivo_instancia = Archivo(
                        nombre=file.name, ruta=file, curso=curso, fecha_publicacion=fecha)
                    if len(file.name) > 50:
                        messages.info(request, 'Nombre de archivo demasiado largo - debe ser menor a 50 caracteres')
                        return HttpResponseRedirect('/curso/' + str(id_curso))
                    if file.name in curso.archivos.values_list('nombre', flat=True) and archivo.nombre != file.name:
                        messages.info(request, 'Archivo repetido - El archivo ya existe en el curso')
                        return HttpResponseRedirect('/curso/' + str(id_curso))
                    else:
                        #añadir archivo
                        try:
                            archivo_instancia.full_clean()
                            #borrar archivo anterior
                            archivo.delete()
                            nombre = archivo.nombre.replace(" ", "_")
                            try:   
                                os.remove("files/" +
                                    str(curso.id) +"/" +  nombre)
                                print("Archivo borrado")
                            except:
                                print("No se pudo borrar el archivo")
                                messages.info(request, 'Error al subir el archivo- Prueba de nuevo en unos minutos')
                                return HttpResponseRedirect('/curso/' + str(id_curso))
                            archivo_instancia.save()
                        except ValidationError as e:
                            excede_mensaje = e.message_dict['ruta'][0]
                            messages.info(request, excede_mensaje)
                            return HttpResponseRedirect('/curso/' + str(id_curso))
    return redirect('/curso/'+str(id_curso))


def sobre_nosotros(request):
    return render(request, "sobre_nosotros.html")


def terminos(request):
    return render(request, "terminos.html")


def privacidad(request):
    return render(request, "privacidad.html")
