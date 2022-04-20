from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.urls import reverse
from app.forms import MonederoForm, UsuarioForm, CursoForm, ReporteForm, UploadFileForm, CursoEditForm, ActualizarUsuarioForm,ComentarioForm, ResponderComentarioForm, ResponderComentarioForm2
from app.models import Usuario, Curso, Archivo, Comentario, Valoracion, Reporte, User, Notificacion
from app.paypal import GetOrder
import json
import os
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
from decouple import config

from django.core.paginator import Paginator


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

                return render(request,"pasarela_pago.html",context={"client_id": client_id,"dinero":dinero})
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
            detalle_precio = float(detalle.result.purchase_units[0].amount.value)

        
        
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
            return cursosdisponibles(request, mensaje_error = True, mensaje = "No puedes suscribirte a este curso")
            
        if usuario in curso_var.suscriptores.all():
            return cursosdisponibles(request, mensaje_error = True, mensaje = "Ya estás suscrito al curso")
            
        if usuario.dinero < Decimal(12.00):
            return cursosdisponibles(request, mensaje_error = True, mensaje = "No tienes dinero suficiente")
            
        else:
            curso_var.suscriptores.add(usuario)
            usuario.dinero -= Decimal(12.00)
            profesor = curso_var.propietario
            profesor.dinero += Decimal(9.00)
            curso_var.save()
            usuario.save()
            profesor.save()
            return curso(request, curso_var.id, suscrito=True)
            
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
        return redirect("/actualizar_perfil")
    else:
        return redirect("/login")


def perfil_usuario(request):
    if request.user.is_authenticated:
        usuarioActual = request.user.usuario

        nombre = request.user.usuario.nombre+' '+request.user.usuario.apellidos
        titulacion = request.user.usuario.titulacion
        dinero = request.user.usuario.dinero

        try:
            foto = request.user.usuario.foto.url
        except:
            foto = "None"

        url = foto.replace("app/static/", "")
        boolPuntos = False

        mediaPuntos = 0
        cursosUsuario = Curso.objects.all().filter(
            propietario=usuarioActual)

        for curso in cursosUsuario:
            valoraciones = Valoracion.objects.all().filter(curso=curso)
            puntos = 0
            for valoracion in valoraciones:
                puntos += valoracion.puntuacion

            if len(valoraciones) > 0:
                mediaPuntos = puntos/len(valoraciones)
                boolPuntos = True
            else:
                mediaPuntos = 0
                
        notificaciones = Notificacion.objects.all().filter(usuario=usuarioActual).order_by('-fecha')

        return render(request, "perfil.html", {"boolPuntos": boolPuntos, "nombre": nombre, "titulacion": titulacion,
                "dinero": dinero, "valoracion": mediaPuntos, "foto": url, "notificaciones": notificaciones})

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
                if(foto != None and os.path.exists('app/static/archivos/'+user_instancia.username+'.jpg')):
                    os.remove("app/static/archivos/" +
                              user_instancia.username + ".jpg")
                    foto.name = username + ".jpg"
                    # save foto in static/archivos
                    path = default_storage.save(
                        foto.name, ContentFile(foto.read()))
                    os.path.join(settings.MEDIA_ROOT, path)
                    check = True

                elif (foto != None and not os.path.exists('app/static/archivos/'+request.user.username+'.jpg')):
                    foto.name = username + ".jpg"
                    # save foto in static/archivos
                    path = default_storage.save(
                        foto.name, ContentFile(foto.read()))
                    os.path.join(settings.MEDIA_ROOT, path)
                    check = True

                elif (foto == None and user_instancia.username != username and os.path.exists('app/static/archivos/'+user_instancia.username+'.jpg')):
                    os.rename("app/static/archivos/" +
                              user_instancia.username + ".jpg", "app/static/archivos/" + username + ".jpg")
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
                form = CursoEditForm(request.POST, instance=curso)
                if form.is_valid():
                    curso_form = form.cleaned_data
                    nombre = curso_form['nombre']
                    descripcion = curso_form['descripcion']
                    curso.nombre = nombre
                    curso.descripcion = descripcion
                    curso.save()
                    return redirect("/inicio_profesor")
                else:
                    return render(request, 'editarcurso.html', {"form": form})
            else:
                form = CursoEditForm(instance=curso)
                return render(request, "editarcurso.html", {"form": form, "curso": curso})
        else:
            return redirect("/miscursos")
    else:
        return redirect("/login")


def curso(request, id, suscrito = False):
    es_owner = False
    es_suscriptor = False

    valoracionCurso = 0

    curso = Curso.objects.get(id=id)
    contenido_curso = Archivo.objects.all().filter(curso=curso)

    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        if usuario.titulacion != curso.asignatura.titulacion and usuario not in curso.suscriptores.all() and usuario != curso.propietario:
            return redirect('/cursosdisponibles')
        form = UploadFileForm(request.POST, request.FILES)
        excede_tamano = False
        excede_mensaje = ""
        valoracionCurso = get_valoracion(curso)
        valoracionUsuario = "No has valorado este curso"
        if curso.propietario == usuario:
            es_owner = True
            if request.method == 'POST':
                if form.is_valid():
                    file = request.FILES['file']
                    curso = Curso.objects.get(id=id)
                    archivo_instancia = Archivo(
                        nombre=file.name, ruta=file, curso=curso)
                    try:
                        archivo_instancia.full_clean()
                        archivo_instancia.save()
                    except ValidationError as e:
                        excede_tamano = True
                        excede_mensaje = e.message_dict['ruta'][0]
                else:
                    form = UploadFileForm()
        elif usuario in curso.suscriptores.all():
            es_suscriptor = True
            try:
                valoracionUsuario = Valoracion.objects.get(
                    curso=curso, usuario=usuario).puntuacion
            except:
                pass

        return render(request, "curso.html", {"id": id, "es_owner": es_owner, "es_suscriptor": es_suscriptor, "curso": curso, "contenido_curso": contenido_curso, "form": form, "excede_tamano": excede_tamano, "excede_mensaje": excede_mensaje, "valoracionCurso": valoracionCurso, "valoracionUsuario": valoracionUsuario, "suscrito": suscrito})

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
            archivo = Archivo.objects.get(id=id_archivo)
            archivo.delete()
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


def cursosdisponibles(request, mensaje_error = False, mensaje = ''):
    if request.user.is_authenticated:
        cursos_todos = Curso.objects.order_by('nombre')
        cursos = []
        usuario_actual = request.user.usuario
        for curso in cursos_todos:
            suscriptores = curso.suscriptores.all()
            if (curso.propietario != usuario_actual):
                if (usuario_actual not in suscriptores and usuario_actual.titulacion == curso.asignatura.titulacion):
                    valoracion = get_valoracion(curso)
                    cursos.append((curso, valoracion))
        page_obj = pagination(request, cursos, 9)
        return render(request, "cursosdisponibles.html", {'page_obj': page_obj, "mensaje_error": mensaje_error, "mensaje": mensaje})
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
    url = archivo.ruta.url.replace("app/static/", "")
    reportes = None
    page_obj = None
    if request.user.is_authenticated:
        # Comprobar si el usuario es profesor
        usuario_autenticado = request.user
        usuario = Usuario.objects.get(django_user=usuario_autenticado)
        if (curso.propietario == usuario):
            reportes = Reporte.objects.all().filter(archivo=archivo)
            page_obj = pagination(request, reportes, 5)
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
                    referencia = '/curso/'+str(id_curso)+'/archivo/'+str(id_archivo)
                    notificacion = Notificacion(referencia=referencia,usuario=curso.propietario, tipo="REPORTE", curso=curso, visto=False)
                    notificacion.save()
                    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))
            elif request.POST['action'] == 'Comentar':
                formComentario = ComentarioForm(request.POST)
                if formComentario.is_valid():
                    comentarioForm = formComentario.cleaned_data
                    texto = comentarioForm['texto']
                    Comentario.objects.create(
                        texto=texto, archivo=archivo, fecha=datetime.datetime.now(), usuario=usuario)
                    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))
            elif request.POST['action'] == 'Responder':
                formRespuesta = ResponderComentarioForm(request.POST)
                if formRespuesta.is_valid():
                    responderForm = formRespuesta.cleaned_data
                    responde_a = responderForm['responde_a']
                    texto = responderForm['texto']
                    Comentario.objects.create(texto=texto, archivo=archivo, fecha=datetime.datetime.now(
                    ), usuario=usuario, responde_a=Comentario.objects.get(id=responde_a))
                    return redirect('/curso/'+str(id_curso)+'/archivo/'+str(id_archivo))
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
            formComentario = ComentarioForm()
            formReporte = ReporteForm()
            formRespuesta = ResponderComentarioForm()
            formRespuesta2 = ResponderComentarioForm2()
            return render(request, "archivo.html", {'pdf': archivo.ruta, 'curso': curso, 'archivo': archivo, 'contenido_curso': contenido_curso, 'respuestasDict': respuestasDict,
                                                    'acceso': acceso, 'comentarios': comentarios, 'url': url, 'formReporte': formReporte, 'page_obj': page_obj, 'es_owner': es_owner,
                                                    'usuario': usuario, 'es_plagio': es_plagio, 'es_error': es_error, 'formComentario': formComentario, 'formRespuesta': formRespuesta, 'formRespuesta2': formRespuesta2})
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


def sobre_nosotros(request):
    return render(request, "sobre_nosotros.html")


def terminos(request):
    return render(request, "terminos.html")


def privacidad(request):
    return render(request, "privacidad.html")
