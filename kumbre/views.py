from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Sugerencia
from .forms import SugerenciaForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Usuario
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .models import Reserva, Cabana
from datetime import date
from django.http import JsonResponse
from .models import Reserva
import json
from datetime import datetime
from django.core.mail import send_mail
from .forms import ReservaForm
from django.contrib.auth import logout

def sugerencias(request):
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            sugerencia = form.save()
            send_mail(
                'Nueva Sugerencia Recibida',
                f"Categoría: {sugerencia.categoria}\n"
                f"Nombre: {sugerencia.nombre}\n"
                f"Correo: {sugerencia.correo}\n"
                f"Sugerencia:\n{sugerencia.sugerencia}",
                'anyelyo1@gmail.com',  # Correo del remitente
                ['anyelyho1@gmail.com'],  # Correo del destinatario
                fail_silently=False,
            )
            messages.success(request,"Tu sugerencia ha sido enviada con éxito.")
            return redirect('sugerencias') 

    else:
        form = SugerenciaForm()

    return render(request, 'sugerencias.html', {'form': form})  # ✅ Asegurar el nombre correcto


def inicio(request):
    usuario_id = request.session.get("usuario_id")
    correo = request.session.get("correo")

    return render(request, "inicio.html", {"correo": correo})

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def mapa(request):
    return render(request, 'mapa.html')

def galeria(request):
    return render(request, 'galeria.html')

def restaurante(request):
    return render(request, 'restaurante.html')

def atracciones(request):
    return render(request, 'atracciones.html')

def gastronomia(request):
    return render(request, 'gastronomia.html')

def restricciones(request):
    return render(request, 'restricciones.html')

def cabañas(request):
    return render(request, 'cabañas.html')

def caba_tabi(request):
    return render(request, 'caba_tabi.html')

def caba_geisha(request):
    return render(request, 'caba_geisha.html')

def caba_bourbon(request):
    return render(request, 'caba_bourbon.html')

def caba_cafetal(request):
    return render(request, 'caba_cafetal.html')

def caba_wush(request):
    return render(request, 'caba_wush.html')

def gracias(request):
    return render(request, 'gracias.html')

from .forms import FormularioRegistro

def registro(request):
    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registro exitoso, Por favor inicia sesión")
            return redirect('iniciar_sesion')
        else:
            for field in form.errors:
                for error in form[field].errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, 'registro.html', {'register_mode': True})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.error(request, "Haz iniciado sesión con exito")
                return redirect('inicio')
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'iniciar_sesion.html', {'register_mode': False})
    


def logout_perfil(request):
    logout(request) # Elimina la sesión del usuario
    return redirect("inicio") 


def hacer_reserva(request):
    cabanas = Cabana.objects.all()
    reservas = Reserva.objects.values("cabana_id", "fecha_reserva")
    fechas_ocupadas = {}

    for reserva in reservas:
        cabana_id = str(reserva["cabana_id"])
        fecha = reserva["fecha_reserva"].strftime("%Y-%m-%d")
        
        if cabana_id not in fechas_ocupadas:
            fechas_ocupadas[cabana_id] = []
        fechas_ocupadas[cabana_id].append(fecha)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para hacer una reserva.")
            return redirect("iniciar_sesion")

        try:
            usuario = Usuario.objects.get(usuario=request.user)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect("iniciar_sesion")

        cabana_id = request.POST.get("cabana")
        fecha_reserva = request.POST.get("fecha_reserva")
        numero_personas = request.POST.get("numero_personas")
        telefono = request.POST.get("telefono")
        comentarios = request.POST.get("comentarios")

        if date.fromisoformat(fecha_reserva) < date.today():
            messages.error(request, "No puedes reservar una fecha pasada.")
            return redirect("reservas")

        try:
            cabana = Cabana.objects.get(id=cabana_id)
        except Cabana.DoesNotExist:
            messages.error(request, "Cabaña no encontrada.")
            return redirect("reservas")

        if fecha_reserva in fechas_ocupadas.get(str(cabana_id), []):
            messages.error(request, "Esta cabaña ya está reservada en esa fecha.")
            return redirect("reservas")

        try:
            reserva = Reserva.objects.create(
                usuario=usuario,
                cabana=cabana,
                fecha_reserva=fecha_reserva,
                numero_personas=numero_personas,
                telefono=telefono,
                comentarios=comentarios,
                estado="pendiente"
            )
            
            send_mail(
                "Nueva Reserva Solicitada",
                f"Un usuario ha solicitado una reserva:\n\n"
                f"Usuario: {request.user.username}\n"
                f"Cabaña: {cabana.nombre}\n"
                f"Fecha: {fecha_reserva}\n"
                f"Número de Personas: {numero_personas}\n"
                f"Teléfono: {telefono}\n"
                f"Comentarios: {comentarios}\n\n"
                "Revisa el panel de administración para aprobar o rechazar la reserva.",
                "anyelyho1@gmail.com",
                ["anyelyho1@gmail.com"],
                fail_silently=False,
            )

            messages.success(request, "Reserva enviada. Espera la confirmación del administrador.")
            return redirect("reservas")
        
        except Exception as e:
            messages.error(request, f"Error al crear la reserva: {str(e)}")
            return redirect("reservas")

    return render(request, "reservas.html", {
        "cabanas": cabanas,
        "fechas_ocupadas": json.dumps(fechas_ocupadas)
    })

def obtener_fechas_ocupadas(request, cabana_id):
    reservas = Reserva.objects.filter(cabana_id=cabana_id, estado="aprobada").values_list("fecha_reserva", flat=True)
    fechas_ocupadas = list(reservas)  # Convertimos a lista
    return JsonResponse({"fechas_ocupadas": fechas_ocupadas})


def fechas_ocupadas(request, cabana_id):
    reservas = Reserva.objects.filter(cabana_id=cabana_id).values_list("fecha_reserva", flat=True)
    fechas_ocupadas = [fecha.strftime("%Y-%m-%d") for fecha in reservas]
    return JsonResponse({"fechas_ocupadas": fechas_ocupadas})