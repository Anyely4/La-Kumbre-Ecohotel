from django import forms
from .models import Sugerencia, Usuario
from .models import Reserva, Cabana
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['username', 'correo', 'sugerencia', 'categoria']

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(max_length=254)
    telefono = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # Primero guardamos el User usando el método save de UserCreationForm
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            # Después de guardar el user, creamos el perfil Usuario
            usuario_profile = Usuario(
                usuario=user,
                telefono=self.cleaned_data["telefono"]
            )
            usuario_profile.save()
            
        return user

    # def save(self, commit=True):
    #     usuario = super().save(commit=False)
    #     usuario.email = self.cleaned_data["email"]
    #     if commit:
    #         usuario.save()
    #         Usuario.objects.create(
    #             usuario=usuario,
    #             numero=self.cleaned_data.get('numero'),
    #             direccion=self.cleaned_data.get('direccion')
    #         )
    #     return usuario

class ReservaForm(forms.ModelForm):
    cabana = forms.ModelChoiceField(
        queryset=Cabana.objects.all(),  # Asegúrate de que aquí se obtienen las cabañas
        empty_label="Selecciona una cabaña",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reserva
        fields = ['usuario', 'cabana', 'fecha_reserva']