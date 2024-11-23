from django import forms
from .models import (
    Cliente
)

class ClienteForm(forms.ModelForm):
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmar Contraseña',
        required=False  # Hacer que no sea obligatorio
    )

    class Meta:
        model = Cliente
        fields = [
            'cedula', 'nombre_completo', 'correo_electronico',
            'contrasena', 'telefono', 'direccion'
        ]
        widgets = {
            'contrasena': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        # Si se pasa un cliente, la contraseña no se puede cambiar (solo en creación)
        cliente = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if cliente:
            self.fields['contrasena'].initial = cliente.contrasena
            self.fields['confirmar_contrasena'].widget = forms.HiddenInput()  # Ocultar el campo de confirmar contrasena

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cleaned_data

