from django.shortcuts import render, redirect
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
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .models import Reserva, Cabana
from datetime import date
from django.http import JsonResponse
import json
from datetime import datetime
from django.core.mail import send_mail
from .forms import ReservaForm
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def sugerencias(request):
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            sugerencia = form.save()
            send_mail(
                'Hola Anyely! Tienes una nueva Sugerencia',
                f"Categoría: {sugerencia.categoria}\n"
                f"Nombre: {sugerencia.username}\n"
                f"Correo: {sugerencia.correo}\n"
                f"Sugerencia:\n{sugerencia.sugerencia}",
                'anyelyo1@gmail.com', 
                ['anyelyho1@gmail.com'],  
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

def perfil(request):
    return render(request, 'perfil.html')

def manual(request):
    return render(request, 'manual.html')

def registro(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        errores = []  # Lista para almacenar errores

        if password != confirm_password:
            errores.append('Las contraseñas no coinciden')
        if User.objects.filter(email=email).exists():
            errores.append('El correo ya está registrado')
        if User.objects.filter(username=username).exists():
            errores.append('El nombre de usuario ya está en uso')

        if errores:
            return render(request, 'iniciar_sesion.html', {
                'register_mode': True,  # Indica que debe mostrar el formulario de registro
                'errores': errores
            })

        # Si no hay errores, crear el usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "¡Registro Exitoso!, Ahora inicia sesión.")
        return redirect('iniciar_sesion')

    return render(request, 'iniciar_sesion.html', {'register_mode': True})



    #     form = FormularioRegistro(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         messages.success(request, "Registro exitoso, Por favor inicia sesión")
    #         return redirect('iniciar_sesion')
    #     else:
    #         for field in form.errors:
    #             for error in form[field].errors:
    #                 messages.error(request, "{field}: {error}")
    # return render(request, 'registro.html', {'register_mode': True})

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
                messages.success(request, f"Hola, {user.username} ¡Haz iniciado sesión en La Kumbre!")
                return redirect('inicio')
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'iniciar_sesion.html', {'register_mode': False})
    


def logout_perfil(request):
    if request.user.is_authenticated:
        nombre_usuario = request.user.username  # Obtiene el nombre del usuario
        messages.success(request, f"Adiós, {nombre_usuario}. ¡Vuelve pronto!")  
    
    logout(request)  # Cierra la sesión
    return redirect("inicio")  # Redirige a la página de inicio


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


@login_required
def eliminar_cuenta(request):
    if request.method == "POST":
        user = request.user
        nombre_usuario = user.username
        
        logout(request)  # Cierra sesión
        request.session.flush()  # Borra la sesión manualmente
        user.delete()  # Ahora elimina el usuario
        
        messages.success(request, f"Adiós, {nombre_usuario}. ¡Tu cuenta ha sido eliminada!")
        return redirect("inicio")

    return redirect("inicio")


from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required


@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener la sesión
            messages.success(request, '¡Tu contraseña ha sido actualizada con éxito!')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'cambiar_contrasena.html', {'form': form})



def restablecer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/contrasena/{uid}/{token}/")
            send_mail(
                "Restablecimiento de Contraseña",
                f"Haz clic en el siguiente enlace para restablecer tu contraseña:\n\n{enlace}",
                "anyelyho@gmail.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "Se ha enviado un enlace a tu correo para restablecer tu contraseña.")
            return redirect("inicio")
        else:
            messages.error(request, "No se encontro un usuario con ese correo electronico.")
            return redirect("restablecer")
        
    return render(request, "restablecer.html")


def contrasena(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contrasena = request.POST["password"]
            user.set_password(nueva_contrasena)
            user.save()
            return redirect("password_changed")
        return render(request, "contrasena.html")
    return redirect("iniciar_sesion")


def password_changed(request):
    return render(request, "password_changed.html")