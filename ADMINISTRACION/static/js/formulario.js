document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // Aplicar estilos a los campos
    function applyFieldStyles() {
        document.querySelectorAll('input, select, textarea').forEach(function(element) {
            element.classList.add('form-control');
            if (element.type === 'file') {
                element.classList.add('form-control-file');
            }
            if (element.parentElement.classList.contains('input-group')) {
                element.style.paddingLeft = '45px';
            }
        });
    }

    const form = document.querySelector('.needs-validation');
    let formChanged = false;
    let isSaving = false;

    // Cambia el estado si hay cambios en el formulario
    form.addEventListener('change', () => formChanged = true);

    // Detecta cuando se da clic en el botón de guardar
    form.querySelector('button[type="submit"]').addEventListener('click', function() {
        isSaving = true;
    });

    // Agrega el evento de confirmación al intentar salir
    window.addEventListener('beforeunload', function(e) {
        if (formChanged && !isSaving) {
            e.preventDefault();
            e.returnValue = '¿Estás seguro de que quieres salir? Los cambios no guardados se perderán.';
        }
    });

    // Validación al enviar el formulario
    form.addEventListener('submit', function(event) {
        let hasError = false;
        
        // Verificar campos numéricos para valores negativos
        document.querySelectorAll('input[type="number"]').forEach(function(input) {
            if (input.value < 0) {
                input.setCustomValidity("No se permiten valores negativos");
                hasError = true;
            } else {
                input.setCustomValidity("");
            }
        });

        if (!form.checkValidity() || hasError) {
            event.preventDefault();
            event.stopPropagation();
            
            // Mostrar mensaje de error
            const firstInvalidField = form.querySelector(':invalid');
            if (firstInvalidField) {
                firstInvalidField.focus();
                const toast = document.createElement('div');
                toast.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 end-0 m-3';
                toast.setAttribute('role', 'alert');
                toast.style.zIndex = '1055'; // Asegúrate de que esté por encima del formulario
                toast.innerHTML = `
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Por favor, complete todos los campos requeridos y asegúrese de que no haya valores negativos
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                document.body.appendChild(toast);
                setTimeout(() => {
                    toast.remove();
                }, 5000);
            }
        }

        form.classList.add('was-validated');
    });

    // Aplicar estilos iniciales
    applyFieldStyles();
});
