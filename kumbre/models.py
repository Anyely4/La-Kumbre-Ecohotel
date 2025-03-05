from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Sugerencia(models.Model):
    CATEGORIAS = [
        ('Servicio', 'Servicio'),
        ('Instalaciones', 'Instalaciones'),
        ('Comida', 'Comida'),
    ]
    
    username = models.CharField(max_length=100)
    correo = models.EmailField()
    sugerencia = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)

    def __str__(self):
        return f"{self.username} - {self.categoria}"
    
class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    telefono = models.CharField(max_length=15)


class Cabana(models.Model):  # Corrige el nombre del modelo
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.nombre
    

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cabana = models.CharField(max_length=100)  # Nombre de la cabaña
    fecha = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) # Precio de la cabaña
    telefono = models.CharField(max_length=15)  # Teléfono del usuario
    numero_personas = models.PositiveIntegerField()  # Número de personas en la reserva
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada')])
    confirmada = models.BooleanField(default=False)  

    class Meta:
        unique_together = ('cabana', 'fecha')

    def clean(self):
        # Si ya existe una reserva para la misma cabana y fecha (excluyendo la misma instancia en caso de edición)
        if Reserva.objects.filter(cabana=self.cabana, fecha=self.fecha).exclude(pk=self.pk).exists():
            raise ValidationError("La cabaña ya está reservada para esa fecha.")

    def __str__(self):
        return f"Reserva de {self.cabana} para {self.fecha}"


class Producto(models.Model):
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Campo para la imagen
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # Campo para saber si el producto está añadido al carrito
    en_carrito = models.BooleanField(default=False)
    # Asociamos el producto al usuario que lo añadió (opcional, según tu lógica)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class CarritoProducto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"
    


class Compra(models.Model):
    METODO_PAGO_CHOICES = [
        ('nequi', 'Nequi'),
        ('daviplata', 'Daviplata'),
        ('bancolombia', 'Bancolombia'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Compra #{self.id} de {self.usuario.username}"
    

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='detalles', on_delete=models.CASCADE)
    # El detalle puede estar asociado a un producto o a una reserva.
    # Se usa SET_NULL para que si se elimina el producto o la reserva, el detalle conserve la información.
    producto = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True)
    reserva = models.ForeignKey('Reserva', on_delete=models.SET_NULL, null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)  # Se puede calcular como precio_unitario * cantidad
    
    def __str__(self):
        if self.producto:
            return f"{self.cantidad} x {self.producto.nombre}"
        elif self.reserva:
            return f"Reserva: {self.reserva.cabana} para {self.reserva.fecha}"
        return "Detalle sin asignar"