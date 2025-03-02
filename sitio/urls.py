"""
URL configuration for sitio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kumbre import views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('inicio'), name='home'),  # Redirigir a inicio
    path('inicio/', views.inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('mapa/', views.mapa, name='mapa'),
    path('galeria/', views.galeria, name='galeria'),
    path("reservas/", views.hacer_reserva, name="reservas"),
    path('sugerencias/', views.sugerencias, name='sugerencias'),
    path('restaurante/', views.restaurante, name='restaurante'),
    path('atracciones/', views.atracciones, name='atracciones'),
    path('productos/', views.lista_productos, name='productos'),
    path('restricciones/', views.restricciones, name='restricciones'),
    path('cabañas/', views.cabañas, name='cabañas'),
    path("iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.logout_perfil, name="logout"),
    path('reservas/', views.hacer_reserva, name='reservas'),
    path('resumen/', views.resumen_compra, name='resumen_compra'),
    path('metodos_pago/', views.metodos_pago, name='metodos_pago'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('fechas_ocupadas/<int:cabana_id>/', views.obtener_fechas_ocupadas, name='fechas_ocupadas'),
    path('perfil/', views.perfil, name='perfil'),
    path('manual/', views.manual, name='manual'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('cambiar_contraseña/', views.cambiar_contrasena, name='cambiar_contraseña'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path('contrasena/<uidb64>/<token>/', views.contrasena, name='contrasena'),
    path('password_changed/', views.password_changed, name='password_changed'),
    path('agregar_producto/<int:producto_id>/', views.agregar_producto_carrito, name='agregar_producto_carrito'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)