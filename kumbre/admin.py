from pyexpat import model
from django.contrib import admin 
from .models import Sugerencia
from .models import Usuario 
from .models import Cabana, Reserva  # Asegúrate de importar el modelo correcto
from .models import Producto
from .models import Compra, DetalleCompra


# Register your models here.

@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ("username", "correo", "categoria")
    search_fields = ("username", "correo", "categoria")


@admin.register(Cabana)
class CabanaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio','created_at')  # Muestra estos campos en la lista
    list_filter = ('created_at',)  


admin.site.register(Usuario) 

class ReservaAdmin(admin.ModelAdmin):
    list_display = ( "cabana", "fecha")  # Muestra estas columnas en la tabla
    list_filter = ('estado',) 

admin.site.register(Reserva, ReservaAdmin)

admin.site.register(Producto)



admin.site.register(Compra)
admin.site.register(DetalleCompra)



from django.contrib import admin
from .models import Cabana, PrecioCabana, Festivo, Reserva

class PrecioCabanaAdmin(admin.ModelAdmin):
    list_display = ('cabana', 'precio_entre_semana', 'precio_fin_semana', 'precio_festivo')
    search_fields = ('cabana__nombre',)

class FestivoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'descripcion')
    list_filter = ('fecha',)
    search_fields = ('descripcion',)

admin.site.register(PrecioCabana, PrecioCabanaAdmin)
admin.site.register(Festivo, FestivoAdmin)