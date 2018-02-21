from django.urls import path
from webbody import views
from webbody.views import *

urlpatterns = [
path('principal/', views.PrincipalList.as_view(),name='inicio'),
path('usuario/user/micontenido', Mycontent,name='micontenido'),
path('principal/inicia-sesion',SignView.as_view(),name='sign_in'),
path('principal/cerrar-sesion',Signoutview.as_view(),name='sign_out'),
path('principal/registro',Registrouservista.as_view(),name='registrar'),
path('principalforo/hilos/(?P<nombre>\d+)/$',Principalforohilo.as_view(),name='forohilos'),
path('principalforo/hilos/crearhilo/(?P<pk>\d+)/$',views.Crearhilovista,name='crearhilo'),
path('principalforo/hilos/hilo/(?P<codigo>\d+)/$',Hilo.as_view(),name='hilo'),
path('usuario/user/(?P<username>\d+)/$',Perfiluser.as_view(),name='perfil'),
path('usuario/user/perfil',views.Adminperfil.as_view(),name='adminperfil'),
path('principaldescargas/hilos/(?P<nombre>\d+)/$',Cuerpodescargas.as_view(),name='forodescargas'),
path('principaldescargas/hilos/crearhilo/(?P<pk>\d+)/$',views.Crearhilodescarga,name='crearhilodescarga'),
path('principaldescargas/hilos/crearhilo/finalizarhilo/(?P<titulo>\d+)/(?P<pk>\d+)/(?P<tpeli>\d+)/$',views.Finalizarhilodescarga,name='finalizarhilo'),
path('principaldescargas/hilos/hilo/(?P<codigo>\d+)/$',Cuerpoforodescargas.as_view(),name='hilodescarga'),
path('principaldescargas/hilos/crearhilo/finalizarhilo/(?P<titulo>\d+)/(?P<pk>\d+)/$',views.Finalizarhilodescjueg,name='finalizarhilojueg'),
path('principaldescargas/hilos/crearhilo/finalizarhilos/(?P<titulo>\d+)/(?P<pk>\d+)/$',views.Finalizarhilodescmus,name='finalizarhilomusica'),
path('usuario/user/modificar/comentario/(?P<id>\d+)/$',Modificarcomentario,name='modcomentario'),
path('usuario/user/eliminar/comentario/(?P<id>\d+)/$',Eliminarcomentario,name='elcomentario'),
path('usuario/user/eliminar/cuenta/',Eliminarcuenta,name='elcuenta'),
path('usuario/user/eliminar/hilo/(?P<titulo>\d+)/$',Eliminarhilo,name='elhilo'),
path('Contacto/', views.Contacto.as_view(), name='contacto'),
]