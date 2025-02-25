from pyexpat import model
from django.contrib import admin 
from .models import Sugerencia
from .models import Usuario 
from .models import Cabana, Reserva  # Asegúrate de importar el modelo correcto



# Register your models here.

@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ("username", "correo", "categoria")
    search_fields = ("username", "correo", "categoria")


@admin.register(Cabana)
class CabanaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created_at')  # Muestra estos campos en la lista
    search_fields = ('nombre',)  # Permite buscar por el campo nombre
    list_filter = ('created_at',)  


admin.site.register(Usuario) 

class ReservaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cabana", "fecha_reserva", "estado")  # Muestra estas columnas en la tabla
    list_filter = ("estado", "cabana", "fecha_reserva")  # Agrega filtros en la barra lateral
    search_fields = ("usuario__username", "cabaña__nombre", "fecha_reserva")  # Permite búsqueda rápida
    list_editable = ("estado",)  # Permite cambiar el estado directamente en la tabla
    ordering = ("-fecha_reserva",)  # Ordena por fecha de reserva (más reciente primero)

admin.site.register(Reserva, ReservaAdmin)

