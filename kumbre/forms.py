from django import forms
from .models import Sugerencia
from .models import Reserva, Cabana

class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['nombre', 'correo', 'sugerencia', 'categoria']



class ReservaForm(forms.ModelForm):
    cabana = forms.ModelChoiceField(
        queryset=Cabana.objects.all(),  # Asegúrate de que aquí se obtienen las cabañas
        empty_label="Selecciona una cabaña",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reserva
        fields = ['usuario', 'cabana', 'fecha_reserva']