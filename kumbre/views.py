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
from django.core.exceptions import ValidationError


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

def spots(request):
    return render(request, 'spots.html')

def columpio(request):
    return render(request, 'columpio.html')
    
    
def confirmacion_compra_usuario(request):
    return render(request, 'confirmacion_compra_usuario.html')

def nueva_compra_admin(request):
    return render(request, 'nueva_compra_admin.html')

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
        fecha_str = request.POST.get("fecha")
        telefono = request.POST.get("telefono")
        tiene_personas_adicionales = request.POST.get("tiene_personas_adicionales", "no")
        personas_adicionales = int(request.POST.get("personas_adicionales", 0)) if tiene_personas_adicionales == "si" else 0
        
        # Validaciones de seguridad
        try:
            # Verificar que la cabaña existe
            cabana = get_object_or_404(Cabana, id=cabana_id)
            
            # Convertir fecha
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Formato de fecha inválido.")
                return redirect('cabanas')
            
            # Verificar que la fecha no es pasada
            if fecha < datetime.now().date():
                messages.error(request, "No se puede reservar en fechas pasadas.")
                return redirect('cabanas')
                
            # Verificar que la fecha no está ocupada (doble verificación)
            if Reserva.objects.filter(cabana=cabana.nombre, fecha=fecha, confirmada=True).exists():
                messages.error(request, "La cabaña ya está reservada para esa fecha.")
                return redirect('cabanas')
            
            # RECALCULAR el precio en el servidor (ignorando cualquier precio enviado por el cliente)
            precios = get_object_or_404(PrecioCabana, cabana=cabana)
            es_festivo = Festivo.objects.filter(fecha=fecha).exists()
            es_fin_semana = fecha.weekday() in [4, 5]  # 5=Sábado, 6=Domingo
            
            if es_festivo:
                precio_base = precios.precio_festivo
                precio_persona_adicional = precios.precio_persona_adicional_finde_festivo
                tipo_dia = 'festivo'
            elif es_fin_semana:
                precio_base = precios.precio_fin_semana
                precio_persona_adicional = precios.precio_persona_adicional_finde_festivo
                tipo_dia = 'fin_semana'
            else:
                precio_base = precios.precio_entre_semana
                precio_persona_adicional = precios.precio_persona_adicional_entre_semana
                tipo_dia = 'entre_semana'
            
            # Calcular precio adicional y total
            precio_adicional = personas_adicionales * float(precio_persona_adicional)
            precio_total = float(precio_base) + precio_adicional
            
            # Crear la reserva con los precios calculados por el servidor
            reserva = Reserva(
                usuario=request.user,
                cabana=cabana.nombre,
                precio=precio_total,  # Precio total calculado en el servidor
                fecha=fecha,
                telefono=telefono, 
                numero_personas="2",  # Base siempre es 2
                personas_adicionales=personas_adicionales,
                precio_personas_adicionales=precio_adicional,
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
            try:
                cabana = get_object_or_404(Cabana, id=cabana_id)
                context["cabana"] = cabana
            except:
                messages.error(request, "Cabaña no encontrada.")
                return redirect('cabanas')
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









from decimal import Decimal
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from decimal import Decimal
import html
from .models import PrecioCabana, Festivo
@login_required
def confirmar_compra(request):
    if request.method == "POST":
        # Añadir esta línea para depuración
        print("Método POST recibido en confirmar_compra")
        print("Datos del formulario:", request.POST)
        print("Archivos:", request.FILES)

        if 'comprobante_pago' not in request.FILES:
            print("⚠️ No se encontró archivo de comprobante_pago en la solicitud")
        
        form = CompraForm(request.POST, request.FILES)
        if form.is_valid():
            print("✅ Formulario válido")
            try:
                # Importar módulo os si no está ya importado en la parte superior del archivo
                import os
                
                # Datos del comprador
                nombre_usuario = form.cleaned_data['nombre']
                email_usuario = form.cleaned_data['email']
                telefono_usuario = form.cleaned_data['telefono']
                metodo_pago = form.cleaned_data['metodo_pago']
                horario_comida = form.cleaned_data.get('horario_comida')
                fecha_entrega = form.cleaned_data.get('fecha_entrega')  # Añadir esta línea para obtener la fecha de entrega
                comprobante_pago = form.cleaned_data.get('comprobante_pago')
                
                # Validar que el método de pago es válido
                metodos_validos = ['nequi', 'daviplata', 'bancolombia']
                if metodo_pago not in metodos_validos:
                    messages.error(request, "Método de pago no válido.")
                    return redirect('metodo_pago')
                
                # Validar el comprobante de pago - MODIFICADO: hacerlo opcional si es necesario
                # o mejorar el mensaje de error para ser más claro
                if not comprobante_pago:
                    messages.error(request, "Por favor, sube el comprobante de pago. Esto es obligatorio para confirmar tu compra.")
                    return redirect('metodo_pago')
                
                # Validar el formato del archivo
                if comprobante_pago:
                    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
                    ext = os.path.splitext(comprobante_pago.name)[1].lower()
                    if ext not in valid_extensions:
                        messages.error(request, f"Formato de archivo no válido: {ext}. Por favor usa JPG, PNG o PDF.")
                        return redirect('metodo_pago')
                    
                    # Validar tamaño (máximo 5MB)
                    if comprobante_pago.size > 5 * 1024 * 1024:  # 5MB en bytes
                        messages.error(request, f"El archivo es demasiado grande ({comprobante_pago.size/1024/1024:.1f}MB). Máximo 5MB.")
                        return redirect('metodo_pago')
                
                # Mapeo de método de pago a código y nombre legible
                METHOD_CODES = {
                    'nequi': 'NEQ001',
                    'daviplata': 'DAV001',
                    'bancolombia': 'BAN001'
                }
                METHOD_NAMES = {
                    'nequi': 'Nequi',
                    'daviplata': 'Daviplata',
                    'bancolombia': 'Bancolombia'
                }
                codigo_metodo = METHOD_CODES.get(metodo_pago, 'UNKNOWN')
                nombre_metodo = METHOD_NAMES.get(metodo_pago, 'Desconocido')
                
                # Recalcular totales en el servidor - No confiar en datos del cliente
                productos = CarritoProducto.objects.filter(usuario=request.user)
                reservas = Reserva.objects.filter(usuario=request.user, confirmada=False)
                
                # Verificación adicional de seguridad: comprobar si aún hay elementos en el carrito
                if not productos.exists() and not reservas.exists():
                    messages.error(request, "No hay productos ni reservas en el carrito para procesar.")
                    return redirect('resumen_compra')
                
                # Total de productos recalculado
                total_productos = 0
                for item in productos:
                    # Obtener el precio actual del producto (por si hubiera cambios)
                    try:
                        producto_actual = get_object_or_404(Producto, id=item.producto.id)
                        total_productos += producto_actual.precio * item.cantidad
                    except Exception as e:
                        messages.error(request, f"Error con el producto {item.producto}: {str(e)}")
                        return redirect('metodo_pago')
                
                # Total de reservas recalculado (validando cada reserva)
                total_reservas = 0
                reservas_validas = []
                
                for reserva in reservas:
                    # Verificar que la cabaña existe
                    try:
                        cabana = Cabana.objects.get(nombre=reserva.cabana)
                        
                        # Verificar que la fecha no esté ocupada por otra reserva confirmada
                        if Reserva.objects.filter(cabana=reserva.cabana, fecha=reserva.fecha, confirmada=True).exists():
                            messages.error(request, f"La cabaña {reserva.cabana} ya no está disponible para el {reserva.fecha}.")
                            continue  # Saltar esta reserva
                            
                        # Recalcular el precio (para evitar manipulaciones)
                        try:
                            precios = PrecioCabana.objects.get(cabana=cabana)
                            es_festivo = Festivo.objects.filter(fecha=reserva.fecha).exists()
                            es_fin_semana = reserva.fecha.weekday() in [5, 6]
                            
                            if es_festivo:
                                precio_base = precios.precio_festivo
                                precio_persona_adicional = precios.precio_persona_adicional_finde_festivo
                            elif es_fin_semana:
                                precio_base = precios.precio_fin_semana
                                precio_persona_adicional = precios.precio_persona_adicional_finde_festivo
                            else:
                                precio_base = precios.precio_entre_semana
                                precio_persona_adicional = precios.precio_persona_adicional_entre_semana
                            
                            precio_adicional = reserva.personas_adicionales * Decimal(str(precio_persona_adicional))
                            precio_total_calculado = Decimal(str(precio_base)) + precio_adicional
                            
                            # Actualizar precio en la reserva (si hubo manipulación)
                            if abs(reserva.precio - precio_total_calculado) > Decimal('0.01'):
                                reserva.precio = precio_total_calculado
                                reserva.save()
                            
                            total_reservas += precio_total_calculado
                            reservas_validas.append(reserva)
                        except PrecioCabana.DoesNotExist:
                            messages.error(request, f"No se encontraron precios para la cabaña {reserva.cabana}.")
                            return redirect('metodo_pago')
                    
                    except Cabana.DoesNotExist:
                        messages.error(request, f"No se encontró la cabaña {reserva.cabana} en la base de datos.")
                        return redirect('metodo_pago')
                    except Exception as e:
                        messages.error(request, f"Error con la reserva de la cabaña {reserva.cabana}: {str(e)}")
                        return redirect('metodo_pago')
                
                # Si no quedan reservas válidas ni productos, redirigir
                if not reservas_validas and not productos.exists():
                    messages.error(request, "No hay productos o reservas válidas para procesar.")
                    return redirect('resumen_compra')
                
                # Total general recalculado
                total = total_productos + total_reservas
                
                # Crear la compra y marcarla como pagada
                try:
                    compra = Compra.objects.create(
                        usuario=request.user,
                        nombre=nombre_usuario,
                        email=email_usuario,
                        telefono=telefono_usuario,
                        total=total,
                        metodo_pago=metodo_pago,
                        horario_comida=horario_comida,
                        fecha_entrega=fecha_entrega,  # Añadir fecha de entrega al objeto compra
                        comprobante_pago=comprobante_pago,
                        pagado=True
                    )
                except Exception as e:
                    messages.error(request, f"Error al crear la compra en la base de datos: {str(e)}")
                    return redirect('metodo_pago')
                
                detalles_compra = []
                productos_compra = []
                
                # Registrar cada producto del carrito en DetalleCompra
                for item in productos:
                    try:
                        producto_actual = get_object_or_404(Producto, id=item.producto.id)
                        DetalleCompra.objects.create(
                            compra=compra,
                            producto=item.producto,
                            precio_unitario=producto_actual.precio,
                            cantidad=item.cantidad,
                            precio_total=item.cantidad * producto_actual.precio
                        )
                        producto_info = {
                            'nombre': item.producto.nombre,
                            'cantidad': item.cantidad,
                            'precio_unitario': producto_actual.precio,
                            'precio_total': item.cantidad * producto_actual.precio
                        }
                        productos_compra.append(producto_info)
                        detalles_compra.append(f"- {item.cantidad}x {item.producto.nombre} - ${item.cantidad * producto_actual.precio}")
                    except Exception as e:
                        # En caso de error, registrar pero continuar con otros productos
                        print(f"Error al procesar producto {item.producto.id}: {str(e)}")
                
                # Registrar cada reserva válida y confirmarla
                reservas_compra = []
                for reserva in reservas_validas:
                    try:
                        DetalleCompra.objects.create(
                            compra=compra,
                            reserva=reserva,
                            precio_unitario=reserva.precio,
                            cantidad=1,
                            precio_total=reserva.precio
                        )
                        reserva.confirmada = True
                        reserva.save()
                        
                        reserva_info = {
                            'cabana': reserva.cabana,
                            'fecha': reserva.fecha,
                            'personas': reserva.numero_personas,
                            'personas_adicionales': reserva.personas_adicionales,
                            'precio': reserva.precio
                        }
                        reservas_compra.append(reserva_info)
                        detalles_compra.append(f"- Reserva en {reserva.cabana} para {reserva.fecha} - ${reserva.precio}")
                    except Exception as e:
                        print(f"Error al procesar reserva {reserva.id}: {str(e)}")
                
                # Vaciar el carrito
                try:
                    productos.delete()
                except Exception as e:
                    print(f"Error al vaciar el carrito: {str(e)}")
                
                # ENVÍO DE CORREOS ELECTRÓNICOS - Manejo de errores mejorado
                try:
                    # 1. Correo al usuario
                    subject_usuario = f'Confirmación de tu compra'
                    
                    # Contexto para el correo del usuario
                    context_usuario = {
                        'nombre': nombre_usuario,
                        'compra_id': compra.id,
                        'productos': productos_compra,
                        'reservas': reservas_compra,
                        'total_productos': total_productos,
                        'total_reservas': total_reservas,
                        'total_general': total,
                        'metodo_pago': nombre_metodo,
                        'codigo_pago': codigo_metodo,
                        'fecha_entrega': fecha_entrega.strftime('%d/%m/%Y') if fecha_entrega else None  # Añadir fecha formateada
                    }
                    if productos_compra and horario_comida:
                        context_usuario['horario_comida'] = horario_comida.strftime('%I:%M %p') if horario_comida else None
                        
                    # Renderizar el HTML del correo del usuario
                    html_message_usuario = render_to_string('emails/confirmacion_compra_usuario.html', context_usuario)
                    plain_message_usuario = f"""
    ¡Hola {nombre_usuario}!

    Gracias por tu compra.

    Detalles de tu pedido:
    {''.join(detalles_compra)}

    Total: ${total}
    Método de pago: {nombre_metodo} (Código: {codigo_metodo})
    {f"Fecha de entrega: {fecha_entrega.strftime('%d/%m/%Y')}" if fecha_entrega else ""}
    {f"Horario de comida: {horario_comida.strftime('%I:%M %p')}" if horario_comida else ""}

    Si tienes alguna pregunta, no dudes en contactarnos.

    Saludos,
    El equipo de Cabañas
    """
                    
                    # Enviar correo al usuario
                    send_mail(
                        subject=subject_usuario,
                        message=plain_message_usuario,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email_usuario],
                        html_message=html_message_usuario,
                        fail_silently=True,  # Cambiado a True para que no falle la compra si hay error de correo
                    )
                    
                    # 2. Correo al administrador
                    admin_email = settings.ADMIN_EMAIL if hasattr(settings, 'ADMIN_EMAIL') else settings.EMAIL_HOST_USER
                    subject_admin = f'Nueva compra: #{compra.id} - {nombre_usuario}'
                    
                    comprobante_url = None
                    if compra.comprobante_pago:
                        comprobante_url = request.build_absolute_uri(compra.comprobante_pago.url)

                    # Contexto para el correo del administrador
                    context_admin = {
                        'compra_id': compra.id,
                        'nombre_cliente': nombre_usuario,
                        'email_cliente': email_usuario,
                        'telefono_cliente': telefono_usuario,
                        'productos': productos_compra,
                        'reservas': reservas_compra,
                        'total_productos': total_productos, 
                        'total_reservas': total_reservas,
                        'total_general': total,
                        'metodo_pago': nombre_metodo,
                        'horario_comida': horario_comida.strftime('%I:%M %p') if horario_comida else None,
                        'fecha_entrega': fecha_entrega.strftime('%d/%m/%Y') if fecha_entrega else None,  # Añadir fecha formateada
                        'fecha_actual': datetime.now().strftime('%d/%m/%Y %H:%M'),
                        'comprobante_url': comprobante_url 
                    }
                    
                    # Renderizar el HTML del correo del administrador
                    html_message_admin = render_to_string('emails/nueva_compra_admin.html', context_admin)
                    plain_message_admin = f"""
    NUEVA COMPRA - #{compra.id}

    DATOS DEL CLIENTE:
    Nombre: {nombre_usuario}
    Email: {email_usuario}
    Teléfono: {telefono_usuario}

    DETALLES DE LA COMPRA:
    {''.join(detalles_compra)}

    Total: ${total}
    Método de pago: {nombre_metodo}
    {f"Fecha de entrega: {fecha_entrega.strftime('%d/%m/%Y')}" if fecha_entrega else ""}
    {f"Horario de comida: {horario_comida.strftime('%I:%M %p')}" if horario_comida else ""}
    Comprobante de pago: {'Adjunto' if comprobante_pago else 'No adjuntado'}

    Esta notificación ha sido generada automáticamente.
    """
                    
                    # Enviar correo al administrador
                    send_mail(
                        subject=subject_admin,
                        message=plain_message_admin,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[admin_email],
                        html_message=html_message_admin,
                        fail_silently=True,  # Cambiado a True para que no falle la compra si hay error de correo
                    )
                except Exception as e:
                    # Si hay error en los correos, solo registrar pero no detener la compra
                    print(f"Error al enviar correos electrónicos: {str(e)}")
                
                # Redireccionar a página de confirmación
                return redirect('compra_confirmada', compra_id=compra.id)
                
            except Exception as e:
                messages.error(request, f"Error al procesar la compra: {str(e)}")
                print("Error detallado:", str(e))  # Para depuración en el servidor
                return redirect('metodos_pago')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
            return redirect('metodos_pago')
    
    return redirect('metodos_pago')













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
        try:
            cabana_id = request.GET.get('cabana_id')
            fecha_str = request.GET.get('fecha')
            personas_adicionales = int(request.GET.get('personas_adicionales', 0))
            
            # Validar datos de entrada
            if not cabana_id or not fecha_str:
                return JsonResponse({'success': False, 'error': 'Parámetros incompletos'}, status=400)
                
            # Validar que la cabaña existe
            try:
                cabana = Cabana.objects.get(id=cabana_id)
                precios = PrecioCabana.objects.get(cabana=cabana)
            except Cabana.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Cabaña no encontrada'}, status=404)
            except PrecioCabana.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Precios no configurados'}, status=404)
            
            # Validar y convertir la fecha
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                
                # Verificar que no es una fecha pasada
                if fecha < datetime.now().date():
                    return JsonResponse({'success': False, 'error': 'No se permite fecha pasada'}, status=400)
                    
                # Verificar que la fecha no está ocupada
                if Reserva.objects.filter(cabana=cabana.nombre, fecha=fecha, confirmada=True).exists():
                    return JsonResponse({'success': False, 'error': 'Fecha no disponible'}, status=400)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Formato de fecha inválido'}, status=400)
            
            # Validar personas adicionales
            if personas_adicionales < 0:
                return JsonResponse({'success': False, 'error': 'Valor inválido para personas adicionales'}, status=400)
            
            # Determinar tipo de día y precios correspondientes
            es_festivo = Festivo.objects.filter(fecha=fecha).exists()
            es_fin_semana = fecha.weekday() in [4, 5]  # 5=Sábado, 6=Domingo
            
            if es_festivo:
                precio_base = precios.precio_festivo
                precio_persona_adicional = precios.precio_persona_adicional_finde_festivo
                tipo_dia = 'festivo'
            elif es_fin_semana:
                precio_base = precios.precio_fin_semana
                precio_persona_adicional = precios.precio_persona_adicional_finde_festivo
                tipo_dia = 'fin_semana'
            else:
                precio_base = precios.precio_entre_semana
                precio_persona_adicional = precios.precio_persona_adicional_entre_semana
                tipo_dia = 'entre_semana'
            
            # Calcular precio total
            precio_adicional = personas_adicionales * float(precio_persona_adicional)
            precio_total = float(precio_base) + precio_adicional
                
            # Devolver la información calculada en el servidor
            return JsonResponse({
                'success': True, 
                'precio_base': float(precio_base),
                'precio_total': float(precio_total),
                'precio_persona_adicional_entre_semana': float(precios.precio_persona_adicional_entre_semana),
                'precio_persona_adicional_finde_festivo': float(precios.precio_persona_adicional_finde_festivo),
                'tipo_dia': tipo_dia
            })
            
        except Exception as e:
            # Log del error para el administrador
            print(f"Error en calcular_precio: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Error al calcular el precio'}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)