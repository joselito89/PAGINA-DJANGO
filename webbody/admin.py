from django.contrib import admin
from webbody.models import *
# Register your models here.

class Plataformaadmin(admin.ModelAdmin):
    model = Plataforma
admin.site.register(Plataforma,Plataformaadmin)




class Tipopeliculaadmin(admin.ModelAdmin):
    list_display = ('codigo','nombre')
    fields = (list_display)
    actions_on_bottom = True
    actions_on_top = False
    readonly_fields = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)


admin.site.register(Tipopelicula,Tipopeliculaadmin)

class Estiloadmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    fields = (list_display)
    ordering = ('nombre',)

admin.site.register(Estilo,Estiloadmin)



class Cathilosadmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre','tipo','imagen')
    fields = (list_display)
    ordering = ('nombre',)

admin.site.register(Categoriahilo,Cathilosadmin)

class Musicadmin(admin.TabularInline):
    model = Musica

class Hilosadmin(admin.ModelAdmin):
    inlines = [Musicadmin]
    list_display = ('titulo','codusuhilo','fechahora','contenido','categoriahilo')
    fields = (list_display)
    ordering = ('titulo',)

admin.site.register(Hilos,Hilosadmin)


class Comentariosadmin(admin.ModelAdmin):
    list_display = ('nombreusuario', 'codigohilo','texto','fechahora')
    fields = (list_display)


admin.site.register(Comentarios,Comentariosadmin)

class Perfiladmin(admin.ModelAdmin):
    list_display = ('usuario', 'imgprincipal','fnacimiento','nacionalidad')
    fields = (list_display)


admin.site.register(Perfil,Perfiladmin)

class Enlacesadmin(admin.ModelAdmin):
    list_display = ('url',)
    fields = (list_display)


admin.site.register(Enlace,Enlacesadmin)

class Pelisadmin(admin.ModelAdmin):
    list_display = ('portada','titulo')
    fields = (list_display)


admin.site.register(Peliculas,Pelisadmin)

class Juegosadmin(admin.ModelAdmin):
    list_display = ('titulo','size','titulohilo')
    fields = (list_display)

admin.site.register(Juegos,Juegosadmin)

class Musicadmin(admin.ModelAdmin):
    list_display = ('tituloalbum','artista')
    fields = (list_display)

admin.site.register(Musica,Musicadmin)