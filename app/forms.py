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

class CursoForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        print(user)
        titulacion_user = Usuario.objects.get(email_academico=user).titulacion
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
        
    