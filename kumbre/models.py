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

# class Usuario(models.Model):
#     nombre = models.CharField(max_length=100)
#     telefono = models.CharField(max_length=15)
#     correo = models.EmailField(unique=True, null=True, blank=True)
#     contraseña = models.CharField(max_length=128, default="defaultpassword")
#     activation_token = models.CharField(max_length=64, unique=True, default=uuid.uuid4().hex)  # Genera un token único



class Cabana(models.Model):  # Corrige el nombre del modelo
    nombre = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cabana = models.ForeignKey(Cabana, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    numero_personas = models.PositiveIntegerField()
    telefono = models.CharField(max_length=15)
    comentarios = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)  # Solo auto_now_add

    class Meta:
        unique_together = ("cabana", "fecha_reserva")

    def __str__(self):
        return f"Reserva de {self.cabana.nombre} - {self.fecha_reserva}"
