from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    imgprincipal=models.ImageField(upload_to='images/',default="images/anonimo.png")
    fnacimiento = models.CharField(max_length=10,null=True,help_text="formato:00/00/0000")
    nacionalidad = models.CharField(max_length=30,null=True,help_text="máximo 30 caracteres")

    def __str__(self):
        return self.usuario.username

@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save,sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.perfil.save()

class Categoriahilo(models.Model):
    eleccion = (('foro','Foro'), ('descargas','Descargas'))
    codigo = models.IntegerField(primary_key=True,help_text="debe ser numérico entero")
    nombre = models.CharField(unique=True,null=False ,max_length=30,help_text="máximo 30 caracteres, no puede haber 2 nombres iguales")
    tipo = models.CharField(unique=False, null = False , max_length=9,choices=eleccion,default='foro')
    imagen = models.ImageField(upload_to='images/',default="images/cancel.png")

class Hilos(models.Model):
    codigo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200,null=False,help_text="máximo 200 caracteres",unique=True)
    fechahora = models.DateTimeField(default=datetime.now, blank=True)
    codusuhilo = models.ForeignKey(Perfil,on_delete=models.CASCADE,null=True)
    contenido = models.CharField(max_length=9999,null=False,blank=False,help_text="Texto libre",default="")
    categoriahilo = models.ForeignKey(Categoriahilo, on_delete=models.CASCADE, null=False, unique=False)


class Comentarios(models.Model):
    nombreusuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    codigohilo = models.ForeignKey(Hilos, on_delete=models.CASCADE)
    texto =  models.CharField(max_length=9999,null=False,help_text="Texto libre")
    fechahora = models.DateTimeField(default=datetime.now, blank=True)

class Enlace(models.Model):
    codigo = models.AutoField(primary_key=True)
    url = models.CharField(null=False,max_length=100,help_text="máximo 100 caracteres(mega)")

class Tipopelicula(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(null=False,unique=False,max_length=20,help_text="máximo 20 caracteres")

class Peliculas(models.Model):
    codigo = models.AutoField(primary_key=True)
    portada = models.ImageField(upload_to='images/',default="images/cancel.png",null=False)
    size = models.CharField(max_length=10,help_text='maximo 10 caracteres')
    titulo = models.CharField(max_length=100,help_text="máximo 100 caracteres")
    fechalanzamiento = models.CharField(max_length=10,null=True,help_text="formato:00/00/0000")
    director = models.CharField(max_length=30,help_text="máximo 30 caracteres")
    duracion = models.CharField(max_length=50,help_text="máximo 50 caracteres")
    sinopsis = models.CharField(max_length=9999,help_text="máximo 300 caracteres")
    personajes = models.CharField(max_length=200,help_text="máximo 200 caracteres")
    tipo = models.ForeignKey(Tipopelicula, on_delete=models.CASCADE)
    titulohilo = models.ForeignKey(Hilos, on_delete=models.CASCADE)
    enlace = models.OneToOneField(Enlace, on_delete=models.CASCADE)

class Plataforma(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20,unique=False,null=False,help_text="máximo 20 caracteres")

class Juegos(models.Model):
    codigo = models.AutoField(primary_key=True)
    portada = models.ImageField(upload_to='images/',default="images/cancel.png",null=False)
    size = models.CharField(max_length=10,help_text='maximo 10 caracteres')
    titulo = models.CharField(max_length=100,help_text="máximo 100 caracteres")
    fechalanzamiento = models.CharField(max_length=10,null=True,help_text="formato:00/00/0000")
    desarrolladora = models.CharField(max_length=30,help_text="máximo 30 caracteres")
    distribuidora = models.CharField(max_length=30, help_text="máximo 30 caracteres")
    sinopsis = models.CharField(max_length=9999,help_text="máximo 9999 caracteres")
    personajes = models.CharField(max_length=200,help_text="máximo 200 caracteres")
    numjugadores = models.IntegerField()
    titulohilo = models.ForeignKey(Hilos, on_delete=models.CASCADE)
    enlace = models.OneToOneField(Enlace, on_delete=models.CASCADE)
    plataforma = models.ManyToManyField(Plataforma)

class Estilo(models.Model):
    codigo =  models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20, unique=False, null=False, help_text="máximo 20 caracteres")

class Musica(models.Model):
    codigo = models.AutoField(primary_key=True)
    portada = models.ImageField(upload_to='images/',default="images/cancel.png")
    size = models.CharField(max_length=10, help_text='maximo 10 caracteres')
    tituloalbum = models.CharField(max_length=100,help_text="máximo 100 caracteres")
    fechalanzamiento = models.CharField(max_length=10,null=True,help_text="formato:00/00/0000")
    artista = models.CharField(max_length=30,help_text="máximo 30 caracteres")
    numcanciones =  models.IntegerField()
    titulohilo = models.ForeignKey(Hilos, on_delete=models.CASCADE)
    enlace = models.OneToOneField(Enlace, on_delete=models.CASCADE)
    estilomusical = models.ManyToManyField(Estilo)

