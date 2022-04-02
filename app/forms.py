from django import forms
from app.models import *
from django.forms import ModelForm

def get_choices():
    try:
        return list(Asignatura.objects.all().values_list('titulacion', flat=True).distinct())
    except:
        return []


class AsignaturaModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(
        attrs={'accept': '.pdf, .mp4'}))


class ReporteForm(forms.Form):
    TIPOS_REPORTE = (
        ("PLAGIO", "PLAGIO"),
        ("ERROR", "ERROR"),
    )
    descripcion = forms.CharField(max_length=500, required=True,widget=forms.Textarea)
    tipo = forms.ChoiceField(choices=TIPOS_REPORTE, widget=forms.Select(attrs={'class':'bootstrap-select'}))


class UsuarioForm(forms.Form):
    titulaciones = get_choices()
    opciones = ( (x,x) for x in titulaciones)

    #atributos
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    confirm_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}))
    name = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    surname = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@domain.com'}))
    email_academico = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'uvus@alum.us.es'}))
    titulacion = forms.ChoiceField(choices=opciones, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción ...'}))


class CursoEditForm(ModelForm):
 
    def __init__(self,  *args, **kwargs):
        super(CursoEditForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['descripcion'].error_messages['required'] = 'Este campo es obligatorio'    
    class Meta:
        model = Curso
        fields = ('nombre', 'descripcion')

class CursoForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        titulacion_user = Usuario.objects.get(django_user=user).titulacion
        asignaturas = Asignatura.objects.filter(titulacion=titulacion_user)
        # asignaturas_choices = tuple((a.id, a.nombre) for a in asignaturas)
        # asignatura = forms.CharField(
        #     label='Elige', widget=forms.Select(choices=asignaturas))
        self.fields['asignatura'] = AsignaturaModelChoiceField(
            asignaturas, widget=forms.Select(attrs={'style': 'width: 100%;', 'class': 'form-control '}))
        self.fields['nombre'] = forms.CharField(
            widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
        self.fields['descripcion'] = forms.CharField(
            widget=forms.Textarea(attrs={'style': 'width: 100%;', 'class': 'form-control', 'rows': "5", 'placeholder': 'Proporciona una breve descripcion'}))

        # mensajes de error
        self.fields['nombre'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['descripcion'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['asignatura'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['asignatura'].error_messages['invalid_choice'] = 'Selecciona una opción válida'

    class Meta:
        model = Curso
        fields = ('nombre', 'descripcion', 'asignatura')
