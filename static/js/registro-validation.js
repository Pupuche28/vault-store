document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup');
    const inputs = form.querySelectorAll('input');
    const password = document.getElementById('contrasena');
    const confirmPassword = document.getElementById('confirmar-contraseña');
    const documentoInput = document.getElementById('documento');
    const telefonoInput = document.getElementById('telefono');

    // Expresiones regulares para validación
    const patterns = {
        nombres: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,50}$/,
        apellidos: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,50}$/,
        email: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/,
        telefono: /^[9]\d{8}$/,
        documento: /^\d{8}$/,
        direccion: /^.{5,100}$/,
        contrasena: /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
    };

    // Mensajes de error personalizados
    const errorMessages = {
        nombres: 'El nombre debe contener solo letras y tener entre 2 y 50 caracteres.',
        apellidos: 'Los apellidos deben contener solo letras y tener entre 2 y 50 caracteres.',
        email: 'Por favor ingrese un correo electrónico válido.',
        telefono: 'El teléfono debe comenzar con 9 y tener 9 dígitos.',
        documento: 'El DNI debe tener exactamente 8 dígitos.',
        direccion: 'La dirección debe tener entre 5 y 100 caracteres.',
        contrasena: 'La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un carácter especial.'
    };

    // Función para validar un campo
    function validateField(input) {
        const pattern = patterns[input.id];
        const errorElement = input.nextElementSibling;
        
        if (pattern && !pattern.test(input.value)) {
            input.classList.add('is-invalid');
            errorElement.textContent = errorMessages[input.id];
            return false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }
    }

    // Función para validar que las contraseñas coincidan
    function validatePasswords() {
        const errorElement = confirmPassword.nextElementSibling;
        
        if (password.value !== confirmPassword.value) {
            confirmPassword.classList.add('is-invalid');
            errorElement.textContent = 'Las contraseñas no coinciden.';
            return false;
        } else {
            confirmPassword.classList.remove('is-invalid');
            confirmPassword.classList.add('is-valid');
            return true;
        }
    }

    // Agregar validación en tiempo real para cada campo
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (input.id === 'confirmar-contraseña') {
                validatePasswords();
            } else {
                validateField(input);
            }
        });

        input.addEventListener('input', function() {
            if (input.classList.contains('is-invalid')) {
                if (input.id === 'confirmar-contraseña') {
                    validatePasswords();
                } else {
                    validateField(input);
                }
            }
        });
    });

    // Validación específica para el campo DNI
    if (documentoInput) {
        documentoInput.addEventListener('input', function(e) {
            // Eliminar cualquier carácter que no sea número
            this.value = this.value.replace(/[^\d]/g, '');
            
            // Limitar a 8 dígitos
            if (this.value.length > 8) {
                this.value = this.value.slice(0, 8);
            }
            
            // Validar el campo
            validateField(this);
        });

        // Prevenir pegado de texto que no sean números
        documentoInput.addEventListener('paste', function(e) {
            e.preventDefault();
            const pastedText = (e.clipboardData || window.clipboardData).getData('text');
            const numbersOnly = pastedText.replace(/[^\d]/g, '').slice(0, 8);
            this.value = numbersOnly;
            validateField(this);
        });
    }

    // Validación específica para el campo TELÉFONO
    if (telefonoInput) {
        telefonoInput.addEventListener('input', function(e) {
            // Eliminar cualquier carácter que no sea número
            this.value = this.value.replace(/[^\d]/g, '');
            // Limitar a 9 dígitos
            if (this.value.length > 9) {
                this.value = this.value.slice(0, 9);
            }
            // Validar el campo
            validateField(this);
        });
        // Prevenir pegado de texto que no sean números
        telefonoInput.addEventListener('paste', function(e) {
            e.preventDefault();
            const pastedText = (e.clipboardData || window.clipboardData).getData('text');
            const numbersOnly = pastedText.replace(/[^\d]/g, '').slice(0, 9);
            this.value = numbersOnly;
            validateField(this);
        });
    }

    // Validar el formulario al enviar
    form.addEventListener('submit', function(e) {
        let isValid = true;

        // Validar todos los campos
        inputs.forEach(input => {
            if (input.id === 'confirmar-contraseña') {
                if (!validatePasswords()) isValid = false;
            } else {
                if (!validateField(input)) isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            // Mostrar mensaje de error general
            const errorDiv = document.createElement('div');
            errorDiv.className = 'alert alert-danger mt-3';
            errorDiv.textContent = 'Por favor, corrija los errores en el formulario antes de continuar.';
            
            // Insertar el mensaje después del formulario
            form.parentNode.insertBefore(errorDiv, form.nextSibling);
            
            // Eliminar el mensaje después de 5 segundos
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }
    });

    // Validación en tiempo real de la contraseña
    password.addEventListener('input', function() {
        const errorElement = this.nextElementSibling.nextElementSibling;
        if (!patterns.contrasena.test(this.value)) {
            this.classList.add('is-invalid');
            errorElement.textContent = errorMessages.contrasena;
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
            errorElement.textContent = '';
        }
    });
}); 