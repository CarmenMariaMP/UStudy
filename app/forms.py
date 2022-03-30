from django import forms
from app.models import *
from django.forms import ModelForm



class AsignaturaModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.nombre

class UploadFileForm(forms.Form):
    file = forms.FileField()
    
class ReporteForm(forms.Form):
    TIPOS_REPORTE =(
        ("PLAGIO", "PLAGIO"),
        ("ERROR", "ERROR"),
    )
    descripcion = forms.CharField(max_length=100, required=False)
    tipo = forms.ChoiceField(choices=TIPOS_REPORTE)

class UsuarioForm(forms.Form):
    titulaciones = list(Asignatura.objects.all().values_list('titulacion', flat=True).distinct())
    opciones = ( (x,x) for x in titulaciones)

    #atributos
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50,widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=50,widget=forms.PasswordInput, required=True)
    name = forms.CharField(max_length=40, required=True)
    surname = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(max_length=254, required=True)
    email_academico = forms.EmailField(max_length=254, required=True)
    titulacion = forms.ChoiceField(choices=opciones, required=True)
    descripcion = forms.CharField(max_length=500, required=False)

class CursoForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        titulacion_user = Usuario.objects.get(django_user=user).titulacion
        asignaturas = Asignatura.objects.filter(titulacion=titulacion_user)
        asignaturas_choices = tuple((a.id,a.nombre) for a in asignaturas)
        self.fields['asignatura'] = AsignaturaModelChoiceField(queryset=Asignatura.objects.filter(titulacion=titulacion_user))

        # mensajes de error
        self.fields['nombre'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['descripcion'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['asignatura'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['asignatura'].error_messages['invalid_choice'] = 'Selecciona una opción válida'
        

    class Meta:
        model = Curso
        fields = ('nombre','descripcion','asignatura')
        
    