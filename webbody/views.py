from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse
from django.views.generic import TemplateView, ListView, View, CreateView, DetailView,DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormMixin
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
import logging

class PrincipalList(ListView):
    model = Categoriahilo
    template_name = 'principal.html'

    def get_context_data(self, **kwargs):  # para añadir queryset al listview
        context = super(PrincipalList, self).get_context_data(**kwargs)
        context['datos2'] = Categoriahilo.objects.all().filter(tipo='descargas')
        context['datostipeli'] = Tipopelicula.objects.all()
        context['datostiplataforma'] = Plataforma.objects.all()
        context['datostimusica'] = Estilo.objects.all()
        return context

    def get_queryset(self):  # para filtrar el listview
        queryset = super(PrincipalList, self).get_queryset()
        return queryset.filter(tipo='foro')


class SignView(LoginView):
    template_name = 'login.html'


class Signoutview(LogoutView):
    pass


class Registrouservista(CreateView):
    model = Perfil
    form_class = Registrouser
    template_name = 'registrousuario.html'

    def form_valid(self, form):
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usu = Perfil(usuario=User.objects.get(username=usuario))
        usu.save()
        usuario = authenticate(username=usuario, password=password)
        login(self.request, usuario)
        return redirect('inicio')


def Crearhilovista(request, pk):
    if request.user.is_authenticated:
        cathilo = Categoriahilo.objects.get(codigo=pk)
        usu = Perfil.objects.get(usuario=request.user.id)
        form = Crearhilo(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                titulo = form.cleaned_data['titulo']
                contenido = form.cleaned_data['contenido']
                hilo = Hilos(titulo=titulo, codusuhilo=usu, contenido=contenido, categoriahilo=cathilo)
                hilo.save()
                url = reverse('forohilos', kwargs={'nombre': cathilo.nombre})
                return HttpResponseRedirect(url)
        form = Crearhilo()
        return render(request, 'crearhilo.html', {'form': form})
    else:
        return HttpResponseRedirect('/principal')


class Principalforohilo(TemplateView):
    model = Hilos
    template_name = 'cuerpoforo.html'

    def get_context_data(self, **kwargs):  # para añadir queryset al listview
        context = super(Principalforohilo, self).get_context_data(**kwargs)
        context.update({
            'query': Categoriahilo.objects.filter(nombre=kwargs['nombre']),
            'query2': Hilos.objects.filter(categoriahilo=Categoriahilo.objects.get(nombre=kwargs['nombre'])),
        })
        return context


class Hilo(FormMixin, ListView):
    model = Hilos
    template_name = 'cuerpohilo.html'
    paginate_by = 3
    form_class = Crearcomentario

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Hilo, self).get_context_data(**kwargs)
        codhilo = Hilos.objects.filter(codigo=self.kwargs['codigo']).values('codusuhilo')
        context['querycomentarios'] = Comentarios.objects.filter(codigohilo=self.kwargs['codigo'])
        context['queryusucoment'] = Comentarios.objects.filter(nombreusuario=codhilo[0]['codusuhilo'])
        return context

    def get_queryset(self, **kwargs):
        return Hilos.objects.filter(codigo=self.kwargs['codigo'])

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cathilo = Hilos.objects.get(codigo=kwargs['codigo'])
            usu = Perfil.objects.get(usuario=request.user.id)
            form = Crearcomentario(request.POST, request.FILES)
            if request.method == 'POST':
                if form.is_valid():
                    texto = form.cleaned_data['texto']
                    hilo = Comentarios(nombreusuario=usu, codigohilo=cathilo, texto=texto)
                    hilo.save()
                    url = reverse('hilo',kwargs={'codigo':cathilo.codigo})
                    return  HttpResponseRedirect(url)
            return render(request,'cuerpohilo.html',{'form':form})
        else:
            return HttpResponseRedirect('/principal')


class Perfiluser(DetailView):
    model = Perfil
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        context = super(Perfiluser, self).get_context_data(**kwargs)
        usu = User.objects.get(username=self.kwargs['username'])
        context['nmensajes'] = Comentarios.objects.filter(nombreusuario=Perfil.objects.get(usuario=usu))
        return context

    def get_object(self, **kwargs):
        usu = User.objects.get(username=self.kwargs['username'])
        return Perfil.objects.filter(usuario=User.objects.get(username=usu))


class Adminperfil(View):

    def get(self, request):
        form = Modificarperfil()
        user = Perfil.objects.filter(usuario=request.user.id)
        return render(request, 'editarperfil.html', {'form': form, 'userr': user})

    def post(self, request):
        us = Perfil.objects.filter(usuario=request.user.id)
        form = Modificarperfil(request.POST, request.FILES)
        if form.is_valid():
            usu = User.objects.get(username=request.user)
            perf = Perfil.objects.get(usuario=usu)

            f_first_name = form.cleaned_data['first_name']
            f_last_name = form.cleaned_data['last_name']
            f_imgprincipal = form.cleaned_data['imgprincipal']
            f_email = form.cleaned_data['email']
            f_password1 = form.cleaned_data['password1']
            f_nacimiento = form.cleaned_data['fnacimiento']
            f_nacionalidad = form.cleaned_data['nacionalidad']

            if f_first_name != usu.first_name and f_first_name != "":
                usu.first_name = f_first_name
            if f_last_name != usu.last_name and f_last_name != "":
                usu.last_name = f_last_name
            if f_email != usu.email and f_email != "":
                usu.email = f_email
            if f_password1 != usu.password and f_password1 != "":
                usu.set_password(f_password1)

            usu.save()

            if f_imgprincipal != perf.imgprincipal and f_imgprincipal:
                perf.imgprincipal = form.cleaned_data['imgprincipal']
            if f_nacimiento != perf.fnacimiento and f_nacimiento != "":
                perf.fnacimiento = f_nacimiento
            if f_nacionalidad != perf.nacionalidad and f_nacionalidad != "":
                perf.nacionalidad = f_nacionalidad

            perf.save()
            return render(request, 'editarperfil.html', {'form': form, 'userr': us, 'modificacion': True})
        form = Modificarperfil(request.POST, request.FILES)
        return render(request, 'editarperfil.html', {'form': form, 'userr': us})


class Cuerpodescargas(ListView):
    model = Categoriahilo
    template_name = 'cuerpoforodescargas.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Cuerpodescargas, self).get_context_data(**kwargs)
        context['cathilo'] = Categoriahilo.objects.filter(nombre=self.kwargs['nombre'])
        context['numhilos'] = Hilos.objects.filter(categoriahilo=Categoriahilo.objects.get(nombre=self.kwargs['nombre']))
        return context

    def get_queryset(self):
        queryset = super(Cuerpodescargas, self).get_queryset()
        return queryset


def Crearhilodescarga(request, pk):
    if request.user.is_authenticated:
        cathilo = Categoriahilo.objects.get(codigo=pk)
        usu = Perfil.objects.get(usuario=request.user.id)
        form = ''
        if cathilo.nombre == 'Peliculas':
            form = Creardescargapeliculas(request.POST, request.FILES)
        elif cathilo.nombre == 'Videogames':
            form = Creardescargajuego(request.POST, request.FILES)
        elif cathilo.nombre == 'Musica':
            form = Creardescargajuego(request.POST,request.FILES)

        if request.method == 'POST':
            if form.is_valid():
                if cathilo.nombre == 'Peliculas':
                    titulo = form.cleaned_data['titulo']
                    contenido = form.cleaned_data['contenido']
                    hilo = Hilos(titulo=titulo, codusuhilo=usu, contenido=contenido, categoriahilo=cathilo)
                    hilo.save()
                    url = reverse('finalizarhilo',
                                  kwargs={'titulo': titulo, 'pk': pk, 'tpeli': form.cleaned_data['categoria'].nombre})
                    return HttpResponseRedirect(url)
                elif cathilo.nombre == 'Videogames':
                    tithilo = form.cleaned_data['titulo']
                    conthilo = form.cleaned_data['contenido']
                    hilo = Hilos(titulo = tithilo,codusuhilo=usu,contenido = conthilo,categoriahilo=cathilo)
                    hilo.save()
                    url = reverse('finalizarhilojueg',kwargs={'titulo':tithilo,'pk':pk})
                    return HttpResponseRedirect(url)
                elif cathilo.nombre == 'Musica':
                    tithilo = form.cleaned_data['titulo']
                    conthilo = form.cleaned_data['contenido']
                    hilo = Hilos(titulo=tithilo, codusuhilo=usu, contenido=conthilo, categoriahilo=cathilo)
                    hilo.save()
                    url = reverse('finalizarhilomusica', kwargs={'titulo': tithilo, 'pk': pk})
                    return HttpResponseRedirect(url)

        if cathilo.nombre == 'Peliculas':
            form = Creardescargapeliculas(request.POST, request.FILES)
        elif cathilo.nombre == 'Videogames':
            form = Creardescargajuego(request.POST, request.FILES)
        elif cathilo.nombre == 'Musica':
            form = Creardescargajuego(request.POST, request.FILES)
        return render(request, 'crearhilodes.html', {'form': form})
    else:
        return HttpResponseRedirect('/principal')


def Finalizarhilodescarga(request, titulo, pk, tpeli):
    cathilo = Categoriahilo.objects.get(codigo=pk)
    tithilo = Hilos.objects.get(titulo=titulo)
    catpeli = Tipopelicula.objects.get(nombre=tpeli)
    if request.user.is_authenticated:
            form = Crearpelicula(request.POST, request.FILES)
            if request.method == 'POST':
                if form.is_valid():
                    if 'gs' in request.POST:
                        portada = form.cleaned_data['portada']
                        peso = form.cleaned_data['peso']
                        title = form.cleaned_data['titulo']
                        flanzamiento = form.cleaned_data['flanzamiento']
                        director = form.cleaned_data['director']
                        duracion = form.cleaned_data['duracion']
                        sinopsis = form.cleaned_data['sinopsis']
                        personajes = form.cleaned_data['actores']
                        enlace = form.cleaned_data['enlace']
                        en = Enlace(url=enlace)
                        en.save()
                        if portada == '':
                            portada = 'images/cancel.png'
                        pel = Peliculas(portada=portada, size=peso, titulo=title, fechalanzamiento=flanzamiento,
                                        director=director, duracion=duracion, sinopsis=sinopsis,
                                        personajes=personajes, tipo=catpeli, titulohilo=tithilo, enlace=en)
                        pel.save()
                        url = reverse('forodescargas', kwargs={'nombre': cathilo.nombre})
                        return HttpResponseRedirect(url)
                    elif 'gi' in request.POST:
                        portada = form.cleaned_data['portada']
                        peso = form.cleaned_data['peso']
                        title = form.cleaned_data['titulo']
                        flanzamiento = form.cleaned_data['flanzamiento']
                        director = form.cleaned_data['director']
                        duracion = form.cleaned_data['duracion']
                        sinopsis = form.cleaned_data['sinopsis']
                        personajes = form.cleaned_data['actores']
                        enlace = form.cleaned_data['enlace']
                        en = Enlace(url=enlace)
                        en.save()
                        if portada == '':
                            portada = 'images/cancel.png'
                        pel = Peliculas(portada=portada, size=peso, titulo=title, fechalanzamiento=flanzamiento,
                                        director=director, duracion=duracion, sinopsis=sinopsis,
                                        personajes=personajes, tipo=catpeli, titulohilo=tithilo, enlace=en)
                        pel.save()
                        return HttpResponseRedirect("")
                    elif 'ca' in request.POST:
                        tithilo.delete()
                        url = reverse('forodescargas', kwargs={'nombre': cathilo.nombre})
                        return HttpResponseRedirect(url)

            return render(request, 'finalizarhilodesc.html', {'title': titulo, 'form': form, 'joder': tpeli})

    else:
        return HttpResponseRedirect('/principal')


class Cuerpoforodescargas(FormMixin, ListView):
    model = Hilos
    template_name = 'cuerpohilodescpelis.html'
    form_class = Crearcomentario

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Cuerpoforodescargas, self).get_context_data(**kwargs)
        codhil = Hilos.objects.get(codigo=self.kwargs['codigo'])
        codhilo = Hilos.objects.filter(codigo=self.kwargs['codigo']).values('codusuhilo')
        context['querycomentarios'] = Comentarios.objects.filter(codigohilo=self.kwargs['codigo'])
        context['queryusucoment'] = Comentarios.objects.filter(nombreusuario=codhilo[0]['codusuhilo'])
        if codhil.categoriahilo.nombre == 'Peliculas':
            context['pelis'] = Peliculas.objects.filter(titulohilo=codhil)
        elif codhil.categoriahilo.nombre == 'Videogames':
            context['vjuegos'] = Juegos.objects.filter(titulohilo=codhil)
        elif codhil.categoriahilo.nombre == 'Musica':
            context['music'] = Musica.objects.filter(titulohilo=codhil)
        return context

    def get_queryset(self, **kwargs):
        return Hilos.objects.filter(codigo=self.kwargs['codigo'])

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cathilo = Hilos.objects.get(codigo=kwargs['codigo'])
            usu = Perfil.objects.get(usuario=request.user.id)
            form = Crearcomentario(request.POST, request.FILES)
            if request.method == 'POST':
                if form.is_valid():
                    texto = form.cleaned_data['texto']
                    hilo = Comentarios(nombreusuario=usu, codigohilo=cathilo, texto=texto)
                    hilo.save()
                    url = reverse('hilodescarga', kwargs={'codigo': cathilo.codigo})
                    return HttpResponseRedirect(url)
            return render(request, 'cuerpohilodescpelis.html', {'form': form})
        else:
            return HttpResponseRedirect('/principal')

def Finalizarhilodescjueg(request,titulo,pk):
    tithilo = Hilos.objects.get(titulo=titulo)
    cathilo = Categoriahilo.objects.get(codigo=pk)
    form = Crearjuego(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            if 'gs' in request.POST:
                portada = form.cleaned_data['portada']
                size = form.cleaned_data['size']
                titulo = form.cleaned_data['titulo']
                fechalanzamiento = form.cleaned_data['fechalanzamiento']
                desarrolladora = form.cleaned_data['desarrolladora']
                distribuidora = form.cleaned_data['distribuidora']
                sinopsis = form.cleaned_data['sinopsis']
                personajes = form.cleaned_data['personajes']
                numjugadores = form.cleaned_data['numerojugadores']
                plataforma = form.cleaned_data['plataforma']
                enlace = Enlace(url=form.cleaned_data['enlace'])
                enlace.save()
                jueg = Juegos(portada=portada, size=size, titulo=titulo, fechalanzamiento=fechalanzamiento,
                              desarrolladora=desarrolladora, distribuidora=distribuidora,
                              sinopsis=sinopsis, personajes=personajes, numjugadores=numjugadores, enlace=enlace,
                              titulohilo=tithilo)
                jueg.save()
                jueg.plataforma.set(plataforma)
                url = reverse('forodescargas', kwargs={'nombre': cathilo.nombre})
                return HttpResponseRedirect(url)
            elif 'gi' in request.POST:
                portada = form.cleaned_data['portada']
                size = form.cleaned_data['size']
                titulo = form.cleaned_data['titulo']
                fechalanzamiento = form.cleaned_data['fechalanzamiento']
                desarrolladora = form.cleaned_data['desarrolladora']
                distribuidora = form.cleaned_data['distribuidora']
                sinopsis = form.cleaned_data['sinopsis']
                personajes = form.cleaned_data['personajes']
                numjugadores = form.cleaned_data['numerojugadores']
                plataforma = form.cleaned_data['plataforma']
                enlace = Enlace(url=form.cleaned_data['enlace'])
                enlace.save()
                jueg = Juegos(portada=portada, size=size, titulo=titulo, fechalanzamiento=fechalanzamiento,
                              desarrolladora=desarrolladora, distribuidora=distribuidora,
                              sinopsis=sinopsis, personajes=personajes, numjugadores=numjugadores, enlace=enlace,
                              titulohilo=tithilo)
                jueg.save()
                jueg.plataforma.set(plataforma)
                return HttpResponseRedirect("")
            elif 'ca' in request.POST:
                tithilo.delete()
                url = reverse('forodescargas', kwargs={'nombre': cathilo.nombre})
                return HttpResponseRedirect(url)


        return HttpResponseRedirect('')
    return render(request,'finalizarhilodesc.html',{'form':form})

def Finalizarhilodescmus(request,titulo,pk):
    tithilo = Hilos.objects.get(titulo=titulo)
    cathilo = Categoriahilo.objects.get(codigo=pk)
    form = Crearmusica(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            if 'gs' in request.POST:
                portada = form.cleaned_data['portada']
                size = form.cleaned_data['size']
                tituloalbum = form.cleaned_data['titulo']
                fechalanzamiento = form.cleaned_data['fechalanzamiento']
                artista = form.cleaned_data['artista']
                numcanciones = form.cleaned_data['numerocanciones']
                estilomusical = form.cleaned_data['estilomusical']
                enlace = Enlace(url=form.cleaned_data['enlace'])
                enlace.save()
                mus = Musica(portada=portada, size=size, tituloalbum=tituloalbum, fechalanzamiento=fechalanzamiento,
                             artista=artista, numcanciones=numcanciones,
                             titulohilo=tithilo, enlace=enlace)
                mus.save()
                mus.estilomusical.set(estilomusical)
                url = reverse('forodescargas', kwargs={'nombre': cathilo.nombre})
                return HttpResponseRedirect(url)
            elif 'gi' in request.POST:
                portada = form.cleaned_data['portada']
                size = form.cleaned_data['size']
                tituloalbum = form.cleaned_data['titulo']
                fechalanzamiento = form.cleaned_data['fechalanzamiento']
                artista = form.cleaned_data['artista']
                numcanciones = form.cleaned_data['numerocanciones']
                estilomusical = form.cleaned_data['estilomusical']
                enlace = Enlace(url=form.cleaned_data['enlace'])
                enlace.save()
                mus = Musica(portada=portada, size=size, tituloalbum=tituloalbum, fechalanzamiento=fechalanzamiento,
                             artista=artista, numcanciones=numcanciones,
                             titulohilo=tithilo, enlace=enlace)
                mus.save()
                mus.estilomusical.set(estilomusical)
                return HttpResponseRedirect("")
            elif 'ca' in request.POST:
                tithilo.delete()
                url = reverse('forodescargas', kwargs={'nombre': cathilo.nombre})
                return HttpResponseRedirect(url)
        return HttpResponseRedirect('')
    return render(request, 'finalizarhilodesc.html', {'form': form})

def Mycontent(request):
    usuario = Perfil.objects.filter(usuario=request.user.id)
    comentarios = Comentarios.objects.filter(nombreusuario=request.user.id)
    hilos = Hilos.objects.filter(codusuhilo=request.user.id)
    return render(request,'contenidouser.html',{'usuario':usuario,'comentarios':comentarios,'hilos':hilos})

def Modificarcomentario(request,id):
    if request.method == 'POST':
        form = Crearcomentario(request.POST,request.FILES)
        if form.is_valid():
            usuario = Perfil.objects.filter(usuario=request.user.id)
            comentarios = Comentarios.objects.filter(nombreusuario=request.user.id)
            hilos = Hilos.objects.filter(codusuhilo=request.user.id)
            text = form.cleaned_data['texto']
            comentario = Comentarios.objects.get(id=id)
            comentario.texto = text
            comentario.save()
            return render(request,'contenidouser.html',{'var':1,'usuario':usuario,'comentarios':comentarios,'hilos':hilos})
        return render(request,'modificarcomentario.html',{'form':form})
    form = Crearcomentario(request.POST, request.FILES)
    return render(request, 'modificarcomentario.html', {'form': form})

def Eliminarcomentario(request,id):
    try:
        usuario = Perfil.objects.filter(usuario=request.user.id)
        comentarios = Comentarios.objects.filter(nombreusuario=request.user.id)
        hilos = Hilos.objects.filter(codusuhilo=request.user.id)
        comentario = Comentarios.objects.get(id=id)
        comentario.delete()
        return render(request, 'contenidouser.html',{'var': 2, 'usuario': usuario, 'comentarios': comentarios, 'hilos': hilos})
    except:
        return HttpResponseRedirect('/principal')

def Eliminarcuenta(request):
    usuario = Perfil.objects.get(usuario=request.user.id)
    user = User.objects.get(username=usuario)
    user.delete()
    return HttpResponseRedirect('/principal')

def Eliminarhilo(request,titulo):
    try:
        hilo = Hilos.objects.get(titulo=titulo)
        hilo.delete()
        usuario = Perfil.objects.filter(usuario=request.user.id)
        comentarios = Comentarios.objects.filter(nombreusuario=request.user.id)
        hilos = Hilos.objects.filter(codusuhilo=request.user.id)
        return render(request, 'contenidouser.html',
                      {'var': 3, 'usuario': usuario, 'comentarios': comentarios, 'hilos': hilos})
    except:
        return HttpResponseRedirect('/principal')

class Contacto(View):
    def get(self, request):
        form = ContactoForm()
        return render(request, 'contactar.html', {'form': form})

    def post(self, request):
        form = ContactoForm(request.POST)
        if form.is_valid():
            asunto = form.cleaned_data['asunto']
            email = form.cleaned_data['email']
            msg = form.cleaned_data['msg'] + '\n\nEmail del usuario: ' + email
            mail = EmailMessage(asunto, msg, email, ['jmarchenaguerrero@gmail.com'])
            mail.send()
        form = ContactoForm()
        return render(request, 'contactar.html', {'form': form})
