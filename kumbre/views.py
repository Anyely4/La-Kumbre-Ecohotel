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
from .models import Reserva, Cabana, Producto
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
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, CarritoProducto
from django.db.models import Sum


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

def lista_productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos de la BD
    return render(request, 'productos.html', {'productos': productos})

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



@login_required
def hacer_reserva(request):
    if request.method == "POST":
        # Obtener los datos del formulario manual
        cabana_valor = request.POST.get("cabana")
        precio = request.POST.get("precio")
        fecha = request.POST.get("fecha")
        telefono = request.POST.get("telefono")
        numero_personas = request.POST.get("numero_personas")
        
        # Aquí podrías agregar validación de los datos recibidos
        
        # Crear y guardar la reserva
        reserva = Reserva(
            usuario=request.user,
            cabana=cabana_valor,  # Asegúrate de que en tu modelo el campo se llama así (sin tilde)
            precio=precio,
            fecha=fecha,
            telefono=telefono,
            numero_personas=numero_personas,
            confirmada=False
        )
        reserva.save()
        messages.success(request, "Reserva añadida al carrito.")
        return redirect('reservas')
    
    else:
        # GET: precargar los datos de la cabaña si se recibe cabana_id en la URL
        cabana_id = request.GET.get("cabana_id")
        context = {}
        if cabana_id:
            cabana = get_object_or_404(Cabana, id=cabana_id)
            context["cabana"] = cabana  # Enviamos la cabaña para precargar el nombre y precio
        return render(request, "reservas.html", context)
    
@login_required
def resumen_compra(request):
    # Reservas pendientes (aún no confirmadas)
    reservas_carrito = Reserva.objects.filter(usuario=request.user, confirmada=False)
    # Productos añadidos al carrito
    productos_carrito = CarritoProducto.objects.filter(usuario=request.user)
    context = {
        'reservas': reservas_carrito,
        'productos': productos_carrito,
    }
    return render(request, 'resumen_compra.html', context)


@login_required
def metodos_pago(request):
    # Aquí puedes implementar la lógica de métodos de pago o mostrar un template placeholder
    return render(request, 'metodos_pago.html')

@login_required
def eliminar_reserva(request, reserva_id):
    # Se obtiene la reserva, asegurándose de que pertenezca al usuario logueado
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    reserva.delete()
    messages.success(request, "Reserva eliminada correctamente.")
    return redirect('resumen_compra')

def obtener_fechas_ocupadas(request, cabana_id):
    reservas = Reserva.objects.filter(cabana__id=cabana_id).values_list('fecha', flat=True)
    fechas_ocupadas = [fecha.strftime("%Y-%m-%d") for fecha in reservas]
    return JsonResponse({'fechas_ocupadas': fechas_ocupadas})



from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        nombre_usuario = user.username
        user.delete()
        messages.success(request, f"Adiós, {nombre_usuario}. ¡Tu cuenta ha sido eliminada con exito!")
        return redirect('home')  # Redirige a la página de inicio después de eliminar la cuenta
    return render(request, 'eliminar_cuenta.html')

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

@login_required
def agregar_producto_carrito(request, producto_id):
    if request.method == "POST":
        producto = get_object_or_404(Producto, id=producto_id)
        # Obtenemos la cantidad enviada, por defecto 1 si no se especifica
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Si el producto ya está en el carrito, actualizamos la cantidad; sino, lo creamos.
        carrito_item, created = CarritoProducto.objects.get_or_create(
            usuario=request.user,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            carrito_item.cantidad += cantidad
            carrito_item.save()
        
        # Opcional: Obtener el total de artículos en el carrito
        total = CarritoProducto.objects.filter(usuario=request.user).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        return JsonResponse({
            'success': True,
            'cart_count': total
        })
    else:
        return JsonResponse({'success': False, 'mensaje': 'Método inválido.'}, status=400)
    

@login_required
def eliminar_producto(request, producto_id):
    if request.method == "POST":
        producto = get_object_or_404(CarritoProducto, id=producto_id, usuario=request.user)
        producto.delete()
        total = CarritoProducto.objects.filter(usuario=request.user).aggregate(
            total=Sum('cantidad')
        )['total'] or 0
        return JsonResponse({'success': True, 'cart_count': total})
    else:
        return JsonResponse({'success': False, 'mensaje': 'Método inválido.'}, status=400)