from select import select
from django import forms
from app.models import *
from django.forms import CharField, ModelForm


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
    descripcion = forms.CharField(max_length=100, required=False)
    tipo = forms.ChoiceField(choices=TIPOS_REPORTE)


class CursoForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        titulacion_user = Usuario.objects.get(django_user=user).titulacion
        asignaturas = Asignatura.objects.filter(titulacion=titulacion_user)
        asignaturas_choices = tuple((a.id, a.nombre) for a in asignaturas)
        # asignatura = forms.CharField(
        #     label='Elige', widget=forms.Select(choices=asignaturas))
        self.fields['asignatura'] = AsignaturaModelChoiceField(
            asignaturas, widget=forms.Select(attrs={'style': 'width: 100%;', 'class': 'form-control '}))
        self.fields['nombre'] = forms.CharField(
            widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
        self.fields['descripcion'] = forms.CharField(
            widget=forms.Textarea(attrs={'style': 'width: 100%;', 'class': 'form-control', 'rows': "3", 'placeholder': 'Proporciona una breve descripcion'}))

        # mensajes de error
        self.fields['nombre'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['descripcion'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['asignatura'].error_messages['required'] = 'Este campo es obligatorio'
        self.fields['asignatura'].error_messages['invalid_choice'] = 'Selecciona una opción válida'

    class Meta:
        model = Curso
        fields = ('nombre', 'descripcion', 'asignatura')
