import args as args
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from webbody.models import Hilos,Comentarios,Tipopelicula,Juegos,Plataforma,Estilo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

class Registrouser(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields= ('username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',)

class Crearhilo(ModelForm):
    class Meta:
        model = Hilos
        fields = ['titulo','contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Escribe aquí...'}),
        }

class Crearcomentario(ModelForm):
    class Meta:
        model = Comentarios
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Escribe aquí tu comentario...'}),
        }

class Modificarperfil(forms.Form):
    first_name = forms.CharField(max_length=150,required=False,help_text='máximo 150 caracteres',label='Nombre')
    last_name = forms.CharField(max_length=150,help_text='máximo 150 caracteres',required=False)
    imgprincipal = forms.ImageField(required=False)
    email = forms.EmailField(max_length=150,help_text='máximo 150 caracteres',required=False)
    password1 = forms.CharField(max_length=150, label='Contraseña', widget=forms.PasswordInput,required=False)
    password2 = forms.CharField(max_length=150, label='Repetir Contraseña', widget=forms.PasswordInput,required=False)
    fnacimiento = forms.CharField(widget=forms.DateInput,required=False)
    nacionalidad = forms.CharField(max_length=150,required=False,help_text='máximo 150 caracteres')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-6'
    helper.field_class = 'col-sm-6'
    helper.layout = Layout(
        Field('nombre', css_class='input-sm'),
        Field('apellidos', css_class='input-sm'),
        Field('imgprincipal', css_class='input-sm'),
        Field('email', css_class='input-sm'),
        Field('contrasena', css_class='input-sm'),
        Field('contrasena2', css_class='input-sm'),
        Field('fnacimiento', css_class='input-sm'),
        Field('nacionalidad', css_class='input-sm'),
        FormActions(Submit('Aceptar', 'Aceptar', css_class='btn-warning'))
    )

    def clean(self):
        if not self.cleaned_data['first_name'] and not self.cleaned_data['last_name'] and not self.cleaned_data['imgprincipal'] and not self.cleaned_data['email']\
                and not self.cleaned_data['password1'] and not self.cleaned_data['password2'] and not self.cleaned_data['fnacimiento'] and not self.cleaned_data['nacionalidad']:
            raise forms.ValidationError('no se ha realizado ningun cambio')
        elif self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('El campo contraseña y repetir contraseña deben coincidir')
        clean_data = self.cleaned_data
        return clean_data

class Modelchoiceformtipopelicula(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.nombre

class Creardescargapeliculas(forms.Form):
    titulo = forms.CharField(max_length=150,required=True,help_text='máximo 150 caracteres',label='Titulo')
    contenido = forms.CharField(max_length=9999,required=False,help_text='máximo 9999 caracteres',label='Contenido',widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Escribe aquí...'}))
    categoria = Modelchoiceformtipopelicula(queryset=Tipopelicula.objects.all(),required=True,widget=forms.Select())

class Crearpelicula(forms.Form):
    portada = forms.ImageField(required=True,label='Carátula')
    peso = forms.CharField(required=True,label='Tamaño Archivo',max_length=10)
    titulo = forms.CharField(max_length=150,label='Título',required=True)
    flanzamiento = forms.DateField(required=True,label='Estreno (mm/dd/yyyy)',widget=forms.DateInput(format="%d/%m/%Y"))
    director = forms.CharField(max_length=50,label='Director',required=True)
    duracion = forms.CharField(max_length=10,label='Duración',required=True)
    sinopsis = forms.CharField(max_length=9999,label='Sinopsis',required=True,widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Escribe aquí la sinopsis...'}))
    actores = forms.CharField(max_length=150,label='Personajes',required=True)
    enlace = forms.CharField(max_length=70,label='Link Descarga (mega)',required=True)

    def clean_enlace(self):
        if  (len(self.cleaned_data['enlace']) < 70 )or ( 'https://mega.nz/#!' not in self.cleaned_data['enlace'] ):
            raise forms.ValidationError('Enlace mega incorrecto')
        return self.cleaned_data['enlace']

    def clean(self):
        clean_data = self.cleaned_data
        return clean_data

class Modelchoiceformplataforma(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
         return obj.nombre

class Creardescargajuego(forms.Form):
    titulo = forms.CharField(max_length=150,required=True,help_text='máximo 150 caracteres',label='Titulo')
    contenido = forms.CharField(max_length=9999,required=False,help_text='máximo 9999 caracteres',label='Contenido',widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Escribe aquí...'}))


class Crearjuego(forms.Form):
    portada = forms.ImageField(required=True,label='Carátula')
    size = forms.CharField(max_length=10,required=True,label='Tamaño')
    titulo = forms.CharField(max_length=150,label='Título del Videojuego',required=True)
    fechalanzamiento = forms.DateField(required=True,label='Lanzamiento (mm/dd/yyyy)',widget=forms.DateInput(format="%d/%m/%Y"))
    desarrolladora = forms.CharField(max_length=150,label='Desarrolladora',required=True)
    distribuidora = forms.CharField(max_length=150, label='Distribuidora', required=True)
    sinopsis = forms.CharField(max_length=9999,label='Sinopsis',required=True,widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Escribe aquí la sinopsis...'}))
    personajes = forms.CharField(max_length=150,label='Personajes',required=True)
    numerojugadores = forms.IntegerField(required=True)
    enlace = forms.CharField(max_length=70,label='Link Descarga (mega)',required=True)
    plataforma = Modelchoiceformplataforma(queryset=Plataforma.objects.all(),required=True)

    def clean_enlace(self):
        if  (len(self.cleaned_data['enlace']) < 70 )or ( 'https://mega.nz/#!' not in self.cleaned_data['enlace'] ):
            raise forms.ValidationError('Enlace mega incorrecto')
        return self.cleaned_data['enlace']

    def clean(self):
        clean_data = self.cleaned_data
        return clean_data

class Modelchoiceformestilo(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
         return obj.nombre


class Crearmusica(forms.Form):
    portada = forms.ImageField(required=True,label='Carátula')
    size = forms.CharField(max_length=10, required=True, label='Tamaño')
    titulo = forms.CharField(max_length=150, label='Título', required=True)
    fechalanzamiento = forms.DateField(required=True, label='Lanzamiento (mm/dd/yyyy)',widget=forms.DateInput(format="%d/%m/%Y"))
    artista = forms.CharField(max_length=50, label='Grupo/Artista', required=True)
    numerocanciones = forms.IntegerField(required=False,label='NºCanciones')
    enlace = forms.CharField(max_length=70, label='Link Descarga (mega)', required=True)
    estilomusical = Modelchoiceformestilo(queryset=Estilo.objects.all(), required=True,label='Estilos')

    def clean(self):
        clean_data = self.cleaned_data
        return clean_data

class ContactoForm(forms.Form):
    asunto = forms.CharField()
    email = forms.EmailField()
    msg = forms.CharField(label='Mensaje', widget=forms.Textarea)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data