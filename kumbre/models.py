from django.db import models
from django.contrib.auth.models import User


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