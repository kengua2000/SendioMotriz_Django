from django import forms
from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
import re

from .models import (
    Cliente,
    Empleado,
    EstadoProductoChoices,
    Producto,
    Proveedor,
    Vehiculo
)

class ClienteForm(forms.ModelForm):
    # Field-level validators
    cedula = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='La cédula debe contener solo números.',
                code='invalid_cedula'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número de cédula'
        })
    )

    nombre_completo = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message='El nombre solo debe contener letras y espacios.',
                code='invalid_name'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre completo'
        })
    )

    correo_electronico = forms.EmailField(
        validators=[EmailValidator(message='Ingrese un correo electrónico válido.')],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )

    contrasena = forms.CharField(
        required=False,  # Cambiado a False para permitir edición sin cambiar contraseña
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres'
        }),
        validators=[MinLengthValidator(8)]
    )

    telefono = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='El número de teléfono debe tener entre 9 y 15 dígitos.',
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: +573001234567'
        })
    )

    direccion = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la dirección completa'
        })
    )

    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre_completo', 'correo_electronico', 'contrasena', 'telefono', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es una edición, establecemos el valor inicial de la contraseña
        if self.instance and self.instance.pk:
            self.fields['cedula'].widget.attrs['readonly'] = True
            self.fields['contrasena'].initial = self.instance.contrasena
            self.fields['contrasena'].widget.render_value = True
           
        

    def clean_contrasena(self):
        """Validación personalizada para la contraseña"""
        contrasena = self.cleaned_data.get('contrasena')
        
        # Si estamos editando y no se proporcionó una nueva contraseña, mantener la actual
        if self.instance and self.instance.pk and not contrasena:
            return self.instance.contrasena
            
        if not contrasena:
            raise ValidationError('La contraseña es requerida.')
            
        if len(contrasena) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
            
        if not re.search(r'[a-z]', contrasena):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
            
        if not re.search(r'\d', contrasena):
            raise ValidationError('La contraseña debe contener al menos un número.')
            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
            raise ValidationError('La contraseña debe contener al menos un carácter especial.')
        
        return contrasena

    def clean_cedula(self):
        """Validación personalizada para la cédula"""
        cedula = self.cleaned_data.get('cedula')
        
        if not cedula.isdigit():
            raise ValidationError('La cédula debe contener solo números.')
            
        if len(cedula) < 5 or len(cedula) > 20:
            raise ValidationError('La longitud de la cédula debe estar entre 5 y 20 dígitos.')
            
        # Verificar si la cédula ya existe
        if Cliente.objects.filter(cedula=cedula).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.cedula != cedula):
                raise ValidationError('Esta cédula ya está registrada.')
        
        return cedula

    def clean_correo_electronico(self):
        """Validación personalizada para el correo electrónico"""
        email = self.cleaned_data.get('correo_electronico')
        
        # Verificar si el correo ya existe
        if Cliente.objects.filter(correo_electronico=email).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.correo_electronico != email):
                raise ValidationError('Este correo electrónico ya está registrado.')
        
        return email

    def clean(self):
        """Validaciones a nivel de formulario"""
        cleaned_data = super().clean()
        nombre_completo = cleaned_data.get('nombre_completo', '')
        
        if nombre_completo:
            # Verificar que el nombre tenga al menos dos palabras
            if len(nombre_completo.split()) < 2:
                self.add_error('nombre_completo', 'Debe ingresar nombre y apellido.')
            
            # Verificar longitud mínima de cada palabra
            for palabra in nombre_completo.split():
                if len(palabra) < 2:
                    self.add_error('nombre_completo', 'Cada palabra debe tener al menos 2 caracteres.')
        
        return cleaned_data

class EmpleadoForm(forms.ModelForm):
    # Field-level validators
    cedula = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='La cédula debe contener solo números.',
                code='invalid_cedula'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número de cédula'
        })
    )

    nombre_completo = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message='El nombre solo debe contener letras y espacios.',
                code='invalid_name'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre completo'
        })
    )

    correo_electronico = forms.EmailField(
        validators=[EmailValidator(message='Ingrese un correo electrónico válido.')],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )

    contrasena = forms.CharField(
        required=False,  # Cambiado a False para permitir edición sin cambiar contraseña
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres'
        }),
        validators=[MinLengthValidator(8)]
    )

    telefono = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='El número de teléfono debe tener entre 9 y 15 dígitos.',
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: +573001234567'
        })
    )

    class Meta:
        model = Empleado
        fields = ['cedula', 'nombre_completo', 'correo_electronico', 'contrasena', 'telefono', 'rol', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es una edición, establecemos el valor inicial de la contraseña
        if self.instance and self.instance.pk:
            self.fields['cedula'].widget.attrs['readonly'] = True
            self.fields['contrasena'].initial = self.instance.contrasena
            self.fields['contrasena'].widget.render_value = True

    def clean_contrasena(self):
        """Validación personalizada para la contraseña"""
        contrasena = self.cleaned_data.get('contrasena')
        
        # Si estamos editando y no se proporcionó una nueva contraseña, mantener la actual
        if self.instance and self.instance.pk and not contrasena:
            return self.instance.contrasena
            
        if not contrasena:
            raise ValidationError('La contraseña es requerida.')
            
        if len(contrasena) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
            
        if not re.search(r'[a-z]', contrasena):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
            
        if not re.search(r'\d', contrasena):
            raise ValidationError('La contraseña debe contener al menos un número.')
            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
            raise ValidationError('La contraseña debe contener al menos un carácter especial.')
        
        return contrasena

    def clean_cedula(self):
        """Validación personalizada para la cédula"""
        cedula = self.cleaned_data.get('cedula')
        
        if not cedula.isdigit():
            raise ValidationError('La cédula debe contener solo números.')
            
        if len(cedula) < 5 or len(cedula) > 20:
            raise ValidationError('La longitud de la cédula debe estar entre 5 y 20 dígitos.')
            
        # Verificar si la cédula ya existe
        if Empleado.objects.filter(cedula=cedula).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.cedula != cedula):
                raise ValidationError('Esta cédula ya está registrada.')
        
        return cedula

    def clean_correo_electronico(self):
        """Validación personalizada para el correo electrónico"""
        email = self.cleaned_data.get('correo_electronico')
        
        # Verificar si el correo ya existe
        if Empleado.objects.filter(correo_electronico=email).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.correo_electronico != email):
                raise ValidationError('Este correo electrónico ya está registrado.')
        
        return email

    def clean(self):
        """Validaciones a nivel de formulario"""
        cleaned_data = super().clean()
        nombre_completo = cleaned_data.get('nombre_completo', '')
        
        if nombre_completo:
            # Verificar que el nombre tenga al menos dos palabras
            if len(nombre_completo.split()) < 2:
                self.add_error('nombre_completo', 'Debe ingresar nombre y apellido.')
            
            # Verificar longitud mínima de cada palabra
            for palabra in nombre_completo.split():
                if len(palabra) < 2:
                    self.add_error('nombre_completo', 'Cada palabra debe tener al menos 2 caracteres.')
        
        return cleaned_data

class ProveedorForm(forms.ModelForm):
    # Field-level validators with enhanced validation patterns
    nombre = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.&-]+$',
                message='El nombre solo debe contener letras, espacios y caracteres especiales permitidos (. & -).',
                code='invalid_name'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del proveedor'
        })
    )

    contacto_nombre = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message='El nombre del contacto solo debe contener letras y espacios.',
                code='invalid_contact_name'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del contacto'
        })
    )

    telefono = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{7,15}$',
                message='El teléfono debe tener entre 7 y 15 dígitos, puede incluir el símbolo + al inicio.',
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: +573001234567'
        })
    )

    correo_electronico = forms.EmailField(
        validators=[EmailValidator(message='Ingrese un correo electrónico válido.')],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )

    direccion = forms.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s,#.-]+$',
                message='La dirección contiene caracteres no permitidos.',
                code='invalid_address'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección completa'
        })
    )

    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto_nombre', 'telefono', 'correo_electronico', 'direccion']
        labels = {
            'nombre': 'Nombre',
            'contacto_nombre': 'Nombre del Contacto',
            'telefono': 'Teléfono',
            'correo_electronico': 'Correo Electrónico',
            'direccion': 'Dirección',
        }

    def clean_nombre(self):
        """Validación personalizada para el nombre del proveedor"""
        nombre = self.cleaned_data.get('nombre')
        
        if not nombre:
            raise forms.ValidationError('El nombre es requerido.')
            
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
            
        # Verificar si el nombre ya existe
        if Proveedor.objects.filter(nombre__iexact=nombre).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.nombre.lower() != nombre.lower()):
                raise forms.ValidationError('Este nombre de proveedor ya está registrado.')
        
        return nombre.strip()

    def clean_contacto_nombre(self):
        """Validación personalizada para el nombre del contacto"""
        contacto_nombre = self.cleaned_data.get('contacto_nombre')
        
        if contacto_nombre:
            if len(contacto_nombre.split()) < 2:
                raise forms.ValidationError('Debe ingresar nombre y apellido del contacto.')
                
            for palabra in contacto_nombre.split():
                if len(palabra) < 2:
                    raise forms.ValidationError('Cada palabra del nombre debe tener al menos 2 caracteres.')
        
        return contacto_nombre.strip() if contacto_nombre else contacto_nombre

    def clean_telefono(self):
        """Validación personalizada para el teléfono"""
        telefono = self.cleaned_data.get('telefono')
        
        if not telefono:
            raise forms.ValidationError('El teléfono es requerido.')
            
        # Eliminar el + inicial si existe para la validación numérica
        numero_limpio = telefono.lstrip('+')
        
        if not numero_limpio.isdigit():
            raise forms.ValidationError('El teléfono solo debe contener números (puede incluir + al inicio).')
            
        if len(numero_limpio) < 7 or len(numero_limpio) > 15:
            raise forms.ValidationError('El teléfono debe tener entre 7 y 15 dígitos.')
        
        return telefono

    def clean_correo_electronico(self):
        """Validación personalizada para el correo electrónico"""
        correo = self.cleaned_data.get('correo_electronico')
        
        if not correo:
            raise forms.ValidationError('El correo electrónico es requerido.')
            
        if not correo.endswith(('.com', '.org', '.net')):
            raise forms.ValidationError('El correo electrónico debe terminar en .com, .org o .net.')
            
        # Verificar si el correo ya existe
        if Proveedor.objects.filter(correo_electronico__iexact=correo).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.correo_electronico.lower() != correo.lower()):
                raise forms.ValidationError('Este correo electrónico ya está registrado.')
        
        return correo.lower()

    def clean_direccion(self):
        """Validación personalizada para la dirección"""
        direccion = self.cleaned_data.get('direccion')
        
        if not direccion:
            raise forms.ValidationError('La dirección es requerida.')
            
        if len(direccion) < 5:
            raise forms.ValidationError('La dirección debe tener al menos 5 caracteres.')
        
        return direccion.strip()

    def clean(self):
        """Validaciones a nivel de formulario"""
        cleaned_data = super().clean()
        
        # Aquí puedes agregar validaciones que involucren múltiples campos
        # Por ejemplo, validar que el correo electrónico del contacto coincida con el dominio de la empresa
        
        return cleaned_data

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-_]+$',
                message='El nombre solo debe contener letras, números, espacios y guiones.',
                code='invalid_name'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del producto'
        })
    )

    marca = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-_]+$',
                message='La marca solo debe contener letras, números, espacios y guiones.',
                code='invalid_brand'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la marca'
        })
    )

    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el precio',
            'min': '0',
            'step': '0.01'
        })
    )

    cantidad = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la cantidad',
            'min': '0'
        })
    )

    color = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message='El color solo debe contener letras y espacios.',
                code='invalid_color'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el color'
        })
    )

    imagen = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'URL de la imagen',
            'rows': 3
        })
    )

    estado = forms.ChoiceField(
        choices=EstadoProductoChoices.choices,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'precio', 'cantidad', 'color', 'imagen', 'estado', 'proveedor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si es una edición, podemos agregar lógica específica aquí si es necesario
            pass

    def clean_nombre(self):
        """Validación personalizada para el nombre del producto"""
        nombre = self.cleaned_data.get('nombre')
        
        if len(nombre.strip()) < 3:
            raise ValidationError('El nombre del producto debe tener al menos 3 caracteres.')
            
        # Verificar si el nombre ya existe
        if Producto.objects.filter(nombre=nombre).exists():
            if not self.instance.pk or (self.instance.pk and self.instance.nombre != nombre):
                raise ValidationError('Ya existe un producto con este nombre.')
        
        return nombre.strip()

    def clean_precio(self):
        """Validación personalizada para el precio"""
        precio = self.cleaned_data.get('precio')
        
        if precio <= 0:
            raise ValidationError('El precio debe ser mayor que 0.')
            
        if precio > 9999999.99:
            raise ValidationError('El precio no puede ser mayor a 9,999,999.99')
        
        return precio

    def clean_cantidad(self):
        """Validación personalizada para la cantidad"""
        cantidad = self.cleaned_data.get('cantidad')
        
        if cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa.')
            
        return cantidad

    def clean(self):
        """Validaciones a nivel de formulario"""
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre', '')
        marca = cleaned_data.get('marca', '')
        
        if nombre and marca:
            # Verificar que el nombre y la marca no sean idénticos
            if nombre.lower() == marca.lower():
                self.add_error('marca', 'La marca no puede ser igual al nombre del producto.')
        
        return cleaned_data
    
class VehiculoForm(forms.ModelForm):
    placa = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9\-]+$',
                message='La placa solo debe contener letras mayúsculas, números y guiones.',
                code='invalid_placa'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la placa del vehículo'
        })
    )
    
    marca = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-_]+$',
                message='La marca solo debe contener letras, números, espacios y guiones.',
                code='invalid_brand'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la marca del vehículo'
        })
    )
    
    modelo = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el modelo del vehículo'
        })
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el precio del vehículo',
            'min': '0',
            'step': '0.01'
        })
    )
    
    color = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message='El color solo debe contener letras y espacios.',
                code='invalid_color'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el color del vehículo'
        })
    )
    
    cantidad = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la cantidad disponible',
            'min': '0'
        })
    )
    
    km_recorridos = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese los kilómetros recorridos',
            'min': '0'
        })
    )
    
    tipo_combustible = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el tipo de combustible'
        })
    )

    imagen = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'URL de la imagen',
            'rows': 3
        })
    )
    
    estado = forms.ChoiceField(
        choices=Vehiculo.EstadoVehiculoChoices.choices,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Vehiculo
        fields = [
            'placa', 'marca', 'modelo', 'precio', 'color', 'cantidad', 
            'km_recorridos', 'tipo_combustible', 'imagen', 'estado', 'proveedor'
        ]
    
    def clean_placa(self):
        placa = self.cleaned_data['placa']
        vehiculo = self.instance

        if vehiculo and vehiculo.placa != placa:
            # Solo validamos la unicidad si la placa ha cambiado
            if Vehiculo.objects.filter(placa=placa).exists():
                raise forms.ValidationError("Ya existe un vehículo con esta placa.")
        return placa
    
    def clean_precio(self):
        """Validación personalizada para el precio"""
        precio = self.cleaned_data.get('precio')
        if precio > 999999999.99:
            raise ValidationError('El precio no puede ser mayor a 999,999,999.99')
        return precio
    
    def clean(self):
        """Validaciones a nivel de formulario"""
        cleaned_data = super().clean()
        marca = cleaned_data.get('marca', '')
        modelo = cleaned_data.get('modelo', '')
        
        if marca and modelo:
            # Verificar que la marca y el modelo no sean idénticos
            if marca.lower() == modelo.lower():
                self.add_error('modelo', 'El modelo no puede ser igual a la marca.')
        
        return cleaned_data


        