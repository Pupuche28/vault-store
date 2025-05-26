document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('signup');
    
    const nombres = document.getElementById('nombres');
    const apellidos = document.getElementById('apellidos');
    const email = document.getElementById('email');
    const telefono = document.getElementById('telefono');
    const documento = document.getElementById('documento');
    const direccion = document.getElementById('direccion');
    const contrasena = document.getElementById('contrasena');
    const confirmarContrasena = document.getElementById('confirmar-contraseña');

    nombres.addEventListener('input', function () {
        validateNombre(nombres);
    });

    apellidos.addEventListener('input', function () {
        validateApellido(apellidos);
    });

    email.addEventListener('input', function () {
        validateEmail(email);
    });

    telefono.addEventListener('input', function () {
        validateTelefono(telefono);
    });

    documento.addEventListener('input', function () {
        validateDocumento(documento);
    });

    direccion.addEventListener('input', function () {
        validateDireccion(direccion);
    });

    contrasena.addEventListener('input', function () {
        validateContrasena(contrasena);
    });

    confirmarContrasena.addEventListener('input', function () {
        validateConfirmarContrasena(contrasena, confirmarContrasena);
    });

    function validateNombre(input) {
        if (input.value.length > 1) {
            setSuccess(input);
        } else {
            setError(input, 'El nombre debe tener al menos 2 caracteres');
        }
    }

    function validateApellido(input) {
        if (input.value.length > 1) {
            setSuccess(input);
        } else {
            setError(input, 'El apellido debe tener al menos 2 caracteres');
        }
    }

    function validateEmail(input) {
        const regex = /^[a-zA-Z0-9._-]+@gmail\.com$/;
        if (regex.test(input.value)) {
            setSuccess(input);
        } else {
            setError(input, 'Ingrese un correo válido con el formato @gmail.com');
        }
    }

    function validateTelefono(input) {
        if (/^\d{9}$/.test(input.value)) {
            setSuccess(input);
        } else {
            setError(input, 'El teléfono debe tener 9 dígitos');
        }
    }

    function validateDocumento(input) {
        if (/^\d{8}$/.test(input.value)) {
            setSuccess(input);
        } else {
            setError(input, 'El número de documento debe tener 8 dígitos');
        }
    }

    function validateDireccion(input) {
        if (input.value.trim().length > 0) {
            setSuccess(input);
        } else {
            setError(input, 'La dirección no puede estar vacía');
        }
    }

    function validateContrasena(input) {
        const regex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$/;
        if (regex.test(input.value)) {
            setSuccess(input);
        } else {
            setError(input, 'La contraseña debe tener al menos 8 caracteres, un número y un carácter especial');
        }
    }

    function validateConfirmarContrasena(passwordInput, confirmInput) {
        if (confirmInput.value === passwordInput.value && confirmInput.value !== "") {
            setSuccess(confirmInput);
        } else {
            setError(confirmInput, 'Las contraseñas no coinciden');
        }
    }

    function setSuccess(input) {
        const formGroup = input.parentElement;
        formGroup.classList.remove('error');
        formGroup.classList.add('success');
    }

    function setError(input, message) {
        const formGroup = input.parentElement;
        formGroup.classList.remove('success');
        formGroup.classList.add('error');
        const small = formGroup.querySelector('small');
        small.innerText = message;
    }
});