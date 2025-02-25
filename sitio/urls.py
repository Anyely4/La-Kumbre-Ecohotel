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
    path('gastronomia/', views.gastronomia, name='gastronomia'),
    path('restricciones/', views.restricciones, name='restricciones'),
    path('cabañas/', views.cabañas, name='cabañas'),
    path('caba_tabi/', views.caba_tabi, name='caba_tabi'),
    path('caba_geisha/', views.caba_geisha, name='caba_geisha'),
    path('caba_bourbon/', views.caba_bourbon, name='caba_bourbon'),
    path('caba_cafetal/', views.caba_cafetal, name='caba_cafetal'),
    path('caba_wush/', views.caba_wush, name='caba_wush'),
    path('gracias/', views.gracias, name='gracias'),
    path("iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.logout_perfil, name="logout"),
    path('fechas_ocupadas/<int:cabaña_id>/', views.obtener_fechas_ocupadas, name='fechas_ocupadas'),
]
