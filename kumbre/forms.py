from django import forms
from .models import Sugerencia, Usuario, Compra

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""
            if 'minlength' in field.widget.attrs:
                del field.widget.attrs['minlength']

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        return new_password1

    def clean(self):
        cleaned_data = self.cleaned_data
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

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


from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['telefono', 'numero_personas', 'fecha']


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['metodo_pago']
        labels = {
            'metodo_pago': 'Método de Pago',
        }
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }
        
from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['nombre', 'email', 'telefono','horario_comida', 'metodo_pago','comprobante_pago', 'fecha_entrega']
        widgets = {
            'metodo_pago': forms.HiddenInput(),
            'horario_comida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }