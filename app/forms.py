from django import forms
from app.models import *
from django.forms import ModelForm

class AsignaturaModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.nombre

class UploadFileForm(forms.Form):
    file = forms.FileField()

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
        
    