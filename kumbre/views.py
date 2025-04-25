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
from django.db.models import Sum, F
from .forms import MetodoPagoForm
from .models import Compra, DetalleCompra
from .forms import CompraForm
from django.db import IntegrityError


def sugerencias(request):
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            sugerencia = form.save()
            
            # Correo para Anyely (administrador)
            send_mail(
                'Hola Anyely! Tienes una nueva Sugerencia📝',
                f"Categoría: {sugerencia.categoria}\n"
                f"Nombre: {sugerencia.username}\n"
                f"Correo: {sugerencia.correo}\n"
                f"Sugerencia:\n{sugerencia.sugerencia}",
                'anyelyo1@gmail.com', 
                ['anyelyho1@gmail.com'],  
                fail_silently=False,
            )
            
            # Correo de confirmación para el usuario
            send_mail(
                'Confirmación de Sugerencia Recibida📝',
                f"Hola {sugerencia.username},\n\n"
                "Gracias por enviar tu sugerencia. Hemos recibido tu mensaje📑 "
                "y lo revisaremos lo antes posible.\n\n"
                "Detalles de tu sugerencia:\n"
                f"Categoría: {sugerencia.categoria}\n"
                f"Sugerencia: {sugerencia.sugerencia}\n\n"
                "Atentamente,\nLa Kumbre.",
                'anyelyo1@gmail.com',  # Tu correo de remitente
                [sugerencia.correo],  # Correo del usuario
                fail_silently=False,
            )
            
            messages.success(request, "Tu sugerencia ha sido enviada con éxito.")
            return redirect('sugerencias') 

    else:
        form = SugerenciaForm()

    return render(request, 'sugerencias.html', {'form': form})

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

def cabanas(request):
    return render(request, 'cabanas.html')

def cabanatabi(request):
    return render(request, 'cabanatabi.html')

def cabanageisha(request):
    return render(request, 'cabanageisha.html')

def cabanacafetal(request):
    return render(request, 'cabanacafetal.html')

def cabanabourbon(request):
    return render(request, 'cabanabourbon.html')

def cabanawush(request):
    return render(request, 'cabanawush.html')

def perfil(request):
    return render(request, 'perfil.html')
    


@login_required
def historial(request):
    # Obtener todas las reservas del usuario (tanto confirmadas como pendientes)
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha')
    
    # Obtener todas las compras del usuario
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    return render(request, 'historial.html', {
        'reservas': reservas,
        'compras': compras
    })
    

def manual(request):
    return render(request, 'manual.html')



def registro(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        telefono = request.POST['telefono']

        # Validaciones
        error = None
        if password != confirm_password:
            error = 'Las contraseñas no coinciden'
        elif User.objects.filter(email=email).exists():
            error = 'El correo ya está registrado'
        elif User.objects.filter(username=username).exists():
            error = 'El nombre de usuario ya está en uso'

        if error:
            messages.error(request, error)
            # En lugar de redirigir, renderizamos la misma plantilla con los datos ingresados
            return render(request, 'iniciar_sesion.html', {
                'register_mode': True,
                'datos_previos': {
                    'username': username,
                    'email': email,
                    'telefono': telefono
                }
            })

        # Si no hay errores, crear el usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        
        messages.success(request, "¡Registro Exitoso!, Ahora inicia sesión.")
        return redirect('iniciar_sesion')

    return render(request, 'iniciar_sesion.html', {'register_mode': True})  


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
        cabana_id = request.POST.get("cabana_id")
        cabana_nombre = request.POST.get("cabana")
        precio = request.POST.get("precio")
        fecha_str = request.POST.get("fecha")
        telefono = request.POST.get("telefono")
        numero_personas = request.POST.get("numero_personas")
        
        # Validaciones de seguridad
        try:
            # Verificar que la cabaña existe
            cabana = get_object_or_404(Cabana, nombre=cabana_nombre)
            if cabana_id and int(cabana_id) != cabana.id:
                messages.error(request, "Datos de cabaña inconsistentes.")
                return redirect('cabanas')
            
            # Convertir fecha
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            # Verificar que la fecha no es pasada
            if fecha < datetime.now().date():
                messages.error(request, "No se puede reservar en fechas pasadas.")
                return redirect('cabanas')
                
            # Verificar que la fecha no está ocupada
            if Reserva.objects.filter(cabana=cabana_nombre, fecha=fecha).exists():
                messages.error(request, "La cabaña ya está reservada para esa fecha.")
                return redirect('cabanas')
                
            # Calcular el precio correcto en el servidor
            precios = get_object_or_404(PrecioCabana, cabana=cabana)
            es_festivo = Festivo.objects.filter(fecha=fecha).exists()
            es_fin_semana = fecha.weekday() == 5
            
            if es_festivo:
                precio_correcto = precios.precio_festivo
            elif es_fin_semana:
                precio_correcto = precios.precio_fin_semana
            else:
                precio_correcto = precios.precio_entre_semana
                
            # Verificar que el precio enviado coincide con el calculado (seguridad adicional)
            if abs(float(precio) - float(precio_correcto)) > 0.01:  # Pequeña tolerancia para errores de redondeo
                messages.error(request, "El precio ha sido modificado. Por favor, inténtelo de nuevo.")
                return redirect('cabanas')
            
            # Crear la reserva
            reserva = Reserva(
                usuario=request.user,
                cabana=cabana_nombre,
                precio=precio_correcto,  # Usar el precio calculado en el servidor
                fecha=fecha,
                telefono=telefono,
                numero_personas=numero_personas,
                estado='Pendiente',
                confirmada=False
            )
            
            reserva.save()
            messages.success(request, "Reserva añadida al carrito, ¿Deseas algo más?")
            return redirect('productos')
            
        except Exception as e:
            messages.error(request, f"Error al procesar la reserva: {str(e)}")
            return redirect('cabanas')
    
    else:
        # Mostrar el formulario con datos precargados si se proporciona una cabaña
        cabana_id = request.GET.get("cabana_id")
        context = {}
        if cabana_id:
            cabana = get_object_or_404(Cabana, id=cabana_id)
            context["cabana"] = cabana
            context["cabana_id"] = cabana_id  # Agregar el ID para usarlo en JavaScript
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
def eliminar_reserva(request, reserva_id):
    # Se obtiene la reserva, asegurándose de que pertenezca al usuario logueado
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    reserva.delete()
    return redirect('resumen_compra')

def obtener_fechas_ocupadas(request, cabana_id):
    # Buscar todas las reservas para esta cabaña
    cabana = get_object_or_404(Cabana, id=cabana_id)
    reservas = Reserva.objects.filter(cabana=cabana.nombre).values_list('fecha', flat=True)
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
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Logging detallado
        print(f"Usuario: {request.user}")
        print(f"Producto: {producto.nombre}")
        print(f"Cantidad: {cantidad}")
        
        # Verificar antes de crear
        existing_cart_item = CarritoProducto.objects.filter(
            usuario=request.user, 
            producto=producto
        ).first()
        
        if existing_cart_item:
            print(f"Producto ya en carrito. Cantidad actual: {existing_cart_item.cantidad}")
            existing_cart_item.cantidad += cantidad
            existing_cart_item.save()
        else:
            nuevo_item = CarritoProducto.objects.create(
                usuario=request.user,
                producto=producto,
                cantidad=cantidad
            )
            print(f"Nuevo item creado: {nuevo_item}")
        
        # Verificar carrito después de modificación
        carrito_actual = CarritoProducto.objects.filter(usuario=request.user)
        print("Carrito actual:")
        for item in carrito_actual:
            print(f"- {item.producto.nombre}: {item.cantidad}")
        
        return JsonResponse({
            'success': True,
            'cart_count': carrito_actual.count()
        })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import CarritoProducto

@login_required
def eliminar_producto(request, producto_id):
    if request.method == "POST":
        try:
            producto = get_object_or_404(CarritoProducto, id=producto_id, usuario=request.user)
            producto.delete()
            
            # Calcular el total de productos en el carrito
            total = CarritoProducto.objects.filter(usuario=request.user).aggregate(
                total=Sum('cantidad')
            )['total'] or 0

            return JsonResponse({'success': True, 'cart_count': total})

        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': f'Error al eliminar: {str(e)}'}, status=500)
    
    return JsonResponse({'success': False, 'mensaje': 'Método inválido.'}, status=400)

    

@login_required
def metodo_pago(request):
    metodo = request.GET.get('metodo', '')
    
    # Obtener productos y reservas de manera expl��cita
    productos = CarritoProducto.objects.filter(usuario=request.user)
    reservas = Reserva.objects.filter(usuario=request.user, confirmada=False)
    
    # Calcular total de productos
    total_productos = productos.aggregate(
        total=Sum(F('cantidad') * F('producto__precio'))
    )['total'] or 0
    
    # Calcular total de reservas
    total_reservas = reservas.aggregate(total=Sum('precio'))['total'] or 0
    
    # Total general
    total_carrito = total_productos + total_reservas
    
    # Crear el formulario con datos iniciales
    form = CompraForm(initial={
        'metodo_pago': metodo,
        'nombre': request.user.first_name,
        'email': request.user.email
    })
    
    context = {
        'form': form,
        'metodo': metodo,
        'productos': productos,
        'reservas': reservas,
        'total_productos': total_productos,
        'total_reservas': total_reservas,
        'total_carrito': total_carrito,
    }
    return render(request, 'metodos_pago.html', context)

@login_required
def confirmar_compra(request):
    """
    Procesa el formulario de compra:
      - Recoge los datos del comprador y el método de pago.
      - Calcula el total sumando los productos en el carrito y las reservas pendientes.
      - Crea la compra y los detalles (DetalleCompra) correspondientes.
      - Confirma las reservas y vacía el carrito.
      - Envía dos correos, uno al usuario y otro al administrador.
      - Redirige a la página de confirmación.
    """
    if request.method == "POST":
        form = CompraForm(request.POST)
        if form.is_valid():
            # Datos del comprador
            nombre_usuario = form.cleaned_data['nombre']
            email_usuario = form.cleaned_data['email']
            telefono_usuario = form.cleaned_data['telefono']
            metodo_pago = form.cleaned_data['metodo_pago']
            
            # Mapeo de método de pago a código
            METHOD_CODES = {
                'nequi': 'NEQ001',
                'daviplata': 'DAV001',
                'bancolombia': 'BAN001'
            }
            codigo_metodo = METHOD_CODES.get(metodo_pago, 'UNKNOWN')
            
            # Total de productos en el carrito
            productos = CarritoProducto.objects.filter(usuario=request.user)
            print("Productos en carrito:", productos.count())
            total_productos = productos.aggregate(
                total=Sum(F('cantidad') * F('producto__precio'))
            )['total'] or 0
            
            # Total de reservas pendientes
            reservas = Reserva.objects.filter(usuario=request.user, confirmada=False)
            print("Reservas pendientes:", reservas.count())
            total_reservas = reservas.aggregate(total=Sum('precio'))['total'] or 0
            
            # Total general
            total = total_productos + total_reservas
            
            # Crear la compra y marcarla como pagada
            compra = Compra.objects.create(
                usuario=request.user,
                nombre=nombre_usuario,
                email=email_usuario,
                telefono=telefono_usuario,
                total=total,
                metodo_pago=metodo_pago,
                pagado=True
            )
            
            detalles_compra = []
            # Registrar cada producto del carrito en DetalleCompra
            for item in productos:
                DetalleCompra.objects.create(
                    compra=compra,
                    producto=item.producto,
                    precio_unitario=item.producto.precio,
                    cantidad=item.cantidad,
                    precio_total=item.cantidad * item.producto.precio
                )
                detalles_compra.append(f"- {item.cantidad}x {item.producto.nombre} - ${item.cantidad * item.producto.precio}")
            
            # Registrar cada reserva y confirmarla
            for reserva in reservas:
                DetalleCompra.objects.create(
                    compra=compra,
                    reserva=reserva,
                    precio_unitario=reserva.precio,
                    cantidad=1,
                    precio_total=reserva.precio
                )
                reserva.confirmada = True
                reserva.save()
                # Dado que 'cabana' es un CharField, usamos el valor directamente
                detalles_compra.append(f"- Reserva en {reserva.cabana} - ${reserva.precio}")
            
            # Vaciar el carrito
            productos.delete()
            
            # Preparar el mensaje de correo para el usuario
            detalles_texto = "\n".join(detalles_compra)
            mensaje_usuario = f"""
Hola {nombre_usuario},

Su compra ha sido recibida y confirmada. A continuación, los detalles:

{detalles_texto}

Total: ${total}
Método de pago: {metodo_pago.upper()} (Código: {codigo_metodo})

Gracias por confiar en nosotros.

Saludos,
La Kumbre.
            """.strip()
            
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail("Confirmación de Compra - La Kumbre", mensaje_usuario, from_email, [email_usuario])
            
            # Enviar correo al administrador (en un correo separado)
            admin_email = getattr(settings, "ADMIN_EMAIL", None)
            if admin_email:
                mensaje_admin = f"""
Nueva compra realizada en La Kumbre:

Cliente: {nombre_usuario}
Correo: {email_usuario}
Teléfono: {telefono_usuario}

Detalles de la compra:
{detalles_texto}

Total: ${total}
Método de pago: {metodo_pago.upper()} (Código: {codigo_metodo})

Por favor, revise el panel de administración para más detalles.
                """.strip()
                send_mail("Nueva Compra Realizada - La Kumbre", mensaje_admin, from_email, [admin_email])
            
            return redirect('compra_confirmada', compra_id=compra.id)
    else:
        form = CompraForm()
    return render(request, 'metodos_pago.html', {'form': form})
    
@login_required
def compra_confirmada(request, compra_id):
    """
    Muestra la confirmación final de la compra, incluyendo detalles y la imagen del método de pago.
    """
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    METHOD_CODES = {
        'nequi': 'NEQ001',
        'daviplata': 'DAV001',
        'bancolombia': 'BAN001'
    }
    codigo_metodo = METHOD_CODES.get(compra.metodo_pago, 'UNKNOWN')
    # Mapeo de método a imagen en static (asegúrate de que estas imágenes existan en static/images/)
    image_mapping = {
        'nequi': 'images/nequi.png',
        'daviplata': 'images/daviplata.png',
        'bancolombia': 'images/bancolombia.png'
    }
    image_url = image_mapping.get(compra.metodo_pago, None)
    context = {
        'compra': compra,
        'codigo_metodo': codigo_metodo,
        'image_url': image_url,
    }
    return render(request, 'compra_confirmada.html', context)
    
    

















# Añadir a views.py
from django.http import JsonResponse
from datetime import datetime
from .models import Cabana, PrecioCabana, Festivo

def calcular_precio(request):
    if request.method == "GET":
        cabana_id = request.GET.get('cabana_id')
        fecha_str = request.GET.get('fecha')
        
        try:
            cabana = Cabana.objects.get(id=cabana_id)
            precios = PrecioCabana.objects.get(cabana=cabana)
            
            # Convertir la fecha de string a objeto date
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            # Verificar si es un día festivo
            es_festivo = Festivo.objects.filter(fecha=fecha).exists()
            
            # Verificar si es fin de semana (5=Sábado, 6=Domingo)
            es_fin_semana = fecha.weekday() == 5
            
            # Determinar el precio según el tipo de día
            if es_festivo:
                precio = precios.precio_festivo
            elif es_fin_semana:
                precio = precios.precio_fin_semana
            else:
                precio = precios.precio_entre_semana
                
            return JsonResponse({
                'success': True, 
                'precio': float(precio),
                'tipo_dia': 'festivo' if es_festivo else ('fin_semana' if es_fin_semana else 'entre_semana')
            })
            
        except (Cabana.DoesNotExist, PrecioCabana.DoesNotExist, ValueError) as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)