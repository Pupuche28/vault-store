document.addEventListener('DOMContentLoaded', function() {
    // Solo mostrar si hay progreso de personalización en localStorage
    function getPersonalizacionState() {
        return JSON.parse(localStorage.getItem('ponchoPersonalizado') || '{}');
    }
    function showToastWithProgress(progress) {
        // Evitar duplicados
        if (document.getElementById('toast-personalizacion')) return;
        let toast = document.createElement('div');
        toast.id = 'toast-personalizacion';
        toast.className = 'toast align-items-center show';
        toast.style.minWidth = '300px';
        toast.style.background = '#fff';
        toast.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
        toast.style.border = '1px solid #ccc';
        toast.style.marginBottom = '1rem';
        toast.innerHTML = `
            <div class="d-flex align-items-center p-2">
                <div class="flex-grow-1">
                    <strong>Subiendo imagen personalizada...</strong>
                    <div class="progress mt-2" style="height: 18px;">
                        <div id="toast-progress-bar-global" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: ${progress}%">${progress}%</div>
                    </div>
                </div>
                <button type="button" class="btn-close ms-2 mb-1" aria-label="Close"></button>
            </div>
        `;
        document.getElementById('toast-container').appendChild(toast);
        toast.querySelector('.btn-close').onclick = function() {
            toast.remove();
            // Limpiar progreso si se cierra manualmente
            const state = getPersonalizacionState();
            delete state.progreso;
            localStorage.setItem('ponchoPersonalizado', JSON.stringify(state));
        };
        return toast;
    }
    // Mostrar si hay progreso guardado
    const state = getPersonalizacionState();
    if (state.progreso && state.progreso < 100) {
        const toast = showToastWithProgress(state.progreso);
        const progressBar = toast.querySelector('#toast-progress-bar-global');
        let progress = state.progreso;
        const interval = setInterval(() => {
            progress += 1;
            progressBar.style.width = progress + '%';
            progressBar.textContent = progress + '%';
            state.progreso = progress;
            localStorage.setItem('ponchoPersonalizado', JSON.stringify(state));
            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    toast.remove();
                    delete state.progreso;
                    localStorage.setItem('ponchoPersonalizado', JSON.stringify(state));
                }, 700);
            }
        }, 100);
    }
}); 