// Previsualización de imagen y texto sobre el poncho
const imgUpload = document.getElementById('img-upload');
const imgPreview = document.getElementById('img-preview');
const textInput = document.getElementById('texto-personalizado');
const textPreview = document.getElementById('text-preview');
const tallaBtns = document.querySelectorAll('.talla-btn');
const precioPoncho = document.getElementById('precio-poncho');
const form = document.getElementById('form-personaliza-poncho');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
let precioActual = 99;
let tallaSeleccionada = 'S';

// Guardar y restaurar estado en localStorage
function savePersonalizacionState(state) {
    localStorage.setItem('ponchoPersonalizado', JSON.stringify(state));
}
function getPersonalizacionState() {
    return JSON.parse(localStorage.getItem('ponchoPersonalizado') || '{}');
}
function clearPersonalizacionState() {
    localStorage.removeItem('ponchoPersonalizado');
}

// Restaurar imagen y texto al cargar la página
window.addEventListener('DOMContentLoaded', function() {
    const state = getPersonalizacionState();
    if (state.imagen) {
        imgPreview.src = state.imagen;
        imgPreview.style.display = 'block';
    }
    if (state.texto) {
        textInput.value = state.texto;
        textPreview.textContent = state.texto;
    }
});

// Guardar texto en localStorage
textInput.addEventListener('input', function() {
    textPreview.textContent = this.value;
    const state = getPersonalizacionState();
    state.texto = this.value;
    savePersonalizacionState(state);
});

// Modificar showToastWithProgress para guardar progreso y mostrar en cualquier página
function showToastWithProgress() {
    let toast = document.createElement('div');
    toast.className = 'toast align-items-center show';
    toast.style.minWidth = '300px';
    toast.style.background = '#fff';
    toast.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
    toast.style.border = '1px solid #ccc';
    toast.style.marginBottom = '1rem';
    toast.innerHTML = `
        <div class="d-flex align-items-center p-2">
            <div class="flex-grow-1">
                <strong>Subiendo imagen...</strong>
                <div class="progress mt-2" style="height: 18px;">
                    <div id="toast-progress-bar" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%">0%</div>
                </div>
            </div>
            <button type="button" class="btn-close ms-2 mb-1" aria-label="Close"></button>
        </div>
    `;
    document.getElementById('toast-container').appendChild(toast);
    toast.querySelector('.btn-close').onclick = function() {
        toast.remove();
        // Si se cierra manualmente, limpiar progreso
        const state = getPersonalizacionState();
        delete state.progreso;
        savePersonalizacionState(state);
    };
    return toast;
}

// Mostrar toast si hay progreso guardado
window.addEventListener('DOMContentLoaded', function() {
    const state = getPersonalizacionState();
    if (state.progreso && state.progreso < 100) {
        const toast = showToastWithProgress();
        const progressBar = toast.querySelector('#toast-progress-bar');
        let progress = state.progreso;
        progressBar.style.width = progress + '%';
        progressBar.textContent = progress + '%';
        const interval = setInterval(() => {
            progress += 1;
            progressBar.style.width = progress + '%';
            progressBar.textContent = progress + '%';
            state.progreso = progress;
            savePersonalizacionState(state);
            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    toast.remove();
                    delete state.progreso;
                    savePersonalizacionState(state);
                }, 700);
            }
        }, 100);
    }
});

// Deshabilitar el botón de submit mientras se sube la imagen
const submitBtn = form.querySelector('button[type="submit"]');

imgUpload.addEventListener('change', function(e) {
    // Limpiar imagen previa
    imgPreview.src = '';
    imgPreview.style.display = 'none';
    const state = getPersonalizacionState();
    delete state.imagen;
    savePersonalizacionState(state);
    // Deshabilitar el botón de submit mientras sube
    if (submitBtn) submitBtn.disabled = true;
    const file = e.target.files[0];
    if (file) {
        // Subir la imagen al servidor
        const formData = new FormData();
        formData.append('file', file);
        // Mostrar toast con barra de progreso
        const toast = showToastWithProgress();
        const progressBar = toast.querySelector('#toast-progress-bar');
        let progress = 0;
        const state = getPersonalizacionState();
        state.progreso = 0;
        savePersonalizacionState(state);
        const interval = setInterval(() => {
            progress += 1;
            progressBar.style.width = progress + '%';
            progressBar.textContent = progress + '%';
            state.progreso = progress;
            savePersonalizacionState(state);
            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    toast.remove();
                    delete state.progreso;
                    savePersonalizacionState(state);
                }, 700);
            }
        }, 100); // 100ms * 100 = 10 segundos

        fetch('/api/upload_personalizacion', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                imgPreview.src = data.url;
                imgPreview.style.display = 'block';
                const state = getPersonalizacionState();
                state.imagen = data.url;
                savePersonalizacionState(state);
                // Habilitar el botón de submit cuando la imagen esté lista
                if (submitBtn) submitBtn.disabled = false;
            } else {
                alert('Error al subir la imagen: ' + (data.error || 'Error desconocido.'));
                if (submitBtn) submitBtn.disabled = false;
            }
        })
        .catch(() => {
            alert('Error al subir la imagen.');
            if (submitBtn) submitBtn.disabled = false;
        });
    } else {
        if (submitBtn) submitBtn.disabled = false;
    }
});

// Selección de talla y precio
function seleccionarTalla(btn) {
    tallaBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    tallaSeleccionada = btn.getAttribute('data-talla');
    precioActual = parseInt(btn.getAttribute('data-precio'));
    precioPoncho.textContent = `S/${precioActual}`;
}
tallaBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        seleccionarTalla(this);
    });
});
// Seleccionar S por defecto
seleccionarTalla(document.querySelector('.talla-btn'));

// Añadir al carrito (único producto personalizado por imagen y texto)
form.addEventListener('submit', function(e) {
    e.preventDefault();
    // Solo permitir si hay imagen personalizada lista
    if (!imgPreview.src || imgPreview.src === '') {
        alert('Primero sube tu imagen personalizada.');
        return;
    }
    const cantidad = parseInt(document.getElementById('cantidad').value);
    const texto = textInput.value;
    const imagenUrl = imgPreview.src;
    const talla = tallaSeleccionada;
    const precio = precioActual;
    const imagenNombre = imagenUrl.split('/').pop();
    const productoDB = {
        nombredeproducto: "Poncho Personalizado",
        autor: "Usuario",
        precio: precio,
        descuento: 0,
        stock: 10,
        nombredeTienda: "Tienda Personalizada",
        descripcion: "Poncho personalizado por el usuario",
        caracteristicas: `Talla: ${talla}, Texto: ${texto}, Imagen: ${imagenNombre}`,
        idCategoria: 4, // Textiles
        imagen: imagenNombre
    };
    // 1. Insertar el producto en la base de datos
    fetch('/producto/api/insertarProducto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productoDB)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 1) {
            // 2. Añadir o actualizar en el carrito (solo uno por imagen+texto)
            const cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
            const existingIndex = cartItems.findIndex(item => item.name === 'Poncho Personalizado' && item.image === imagenUrl && item.subname === texto);
            const idProducto = data.data && data.data.idProducto ? data.data.idProducto : null;
            if (existingIndex !== -1) {
                // Si ya existe, solo actualiza la cantidad
                cartItems[existingIndex].quantity += cantidad;
            } else {
                const producto = {
                    id: 'poncho_personalizado_' + Date.now(),
                    idProducto: idProducto,
                    name: 'Poncho Personalizado',
                    subname: texto,
                    price: precio,
                    image: imagenUrl,
                    quantity: cantidad,
                    talla: talla,
                    personalizado: true
                };
                cartItems.push(producto);
            }
            localStorage.setItem('cartItems', JSON.stringify(cartItems));
            if (window.showToast) {
                window.showToast('Poncho personalizado agregado al carrito');
            } else {
                alert('Poncho personalizado agregado al carrito');
            }
            // Mostrar mensaje y redirigir tras 1 segundo
            const msg = document.createElement('div');
            msg.textContent = 'Producto agregado, redirigiendo al carrito...';
            msg.style.position = 'fixed';
            msg.style.top = '30px';
            msg.style.left = '50%';
            msg.style.transform = 'translateX(-50%)';
            msg.style.background = '#222';
            msg.style.color = '#fff';
            msg.style.padding = '16px 32px';
            msg.style.borderRadius = '8px';
            msg.style.zIndex = '9999';
            document.body.appendChild(msg);
            setTimeout(() => {
                msg.remove();
                window.location.href = '/carrito';
            }, 1000);
        } else {
            alert('Error al registrar el producto personalizado: ' + data.message);
        }
    })
    .catch(err => {
        alert('Error al registrar el producto personalizado');
    });
}); 