class UploadHandler {
    constructor() {
        this.uploadInProgress = false;
        this.progressInterval = null;
        this.uploadStartTime = null;
        this.uploadDuration = 10000; // 10 segundos
        this.checkUploadStatus();
    }

    createNotification() {
        const notification = document.createElement('div');
        notification.className = 'upload-notification';
        notification.innerHTML = `
            <div class="upload-notification-header">
                <h5 class="upload-notification-title">Subiendo archivo...</h5>
                <button class="upload-notification-close">&times;</button>
            </div>
            <div class="upload-notification-progress">
                <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                         role="progressbar" 
                         style="width: 0%">0%</div>
                </div>
            </div>
            <div class="upload-notification-file"></div>
        `;
        document.body.appendChild(notification);
        return notification;
    }

    showNotification(fileName) {
        let notification = document.querySelector('.upload-notification');
        if (!notification) {
            notification = this.createNotification();
        }

        notification.querySelector('.upload-notification-file').textContent = fileName;
        notification.classList.add('show');

        // Manejar el botón de cerrar
        notification.querySelector('.upload-notification-close').onclick = () => {
            this.hideNotification();
        };
    }

    hideNotification() {
        const notification = document.querySelector('.upload-notification');
        if (notification) {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }

    updateProgress(progress) {
        const progressBar = document.querySelector('.upload-notification .progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
            progressBar.textContent = `${Math.round(progress)}%`;
        }
    }

    startUpload(file) {
        this.uploadInProgress = true;
        this.uploadStartTime = Date.now();
        this.showNotification(file.name);

        // Guardar el estado en localStorage
        localStorage.setItem('uploadInProgress', 'true');
        localStorage.setItem('uploadFileName', file.name);
        localStorage.setItem('uploadStartTime', this.uploadStartTime.toString());

        // Iniciar la simulación de progreso
        this.startProgressSimulation();
    }

    startProgressSimulation() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }

        this.progressInterval = setInterval(() => {
            const elapsed = Date.now() - this.uploadStartTime;
            const progress = Math.min((elapsed / this.uploadDuration) * 100, 100);
            this.updateProgress(progress);

            if (progress >= 100) {
                this.completeUpload();
            }
        }, 100);
    }

    completeUpload() {
        clearInterval(this.progressInterval);
        this.uploadInProgress = false;
        localStorage.removeItem('uploadInProgress');
        localStorage.removeItem('uploadFileName');
        localStorage.removeItem('uploadStartTime');
        
        // Mostrar mensaje de éxito
        const notification = document.querySelector('.upload-notification');
        if (notification) {
            notification.querySelector('.upload-notification-title').textContent = '¡Archivo subido!';
            setTimeout(() => {
                this.hideNotification();
            }, 2000);
        }
    }

    checkUploadStatus() {
        const uploadInProgress = localStorage.getItem('uploadInProgress') === 'true';
        if (uploadInProgress) {
            const fileName = localStorage.getItem('uploadFileName');
            const startTime = parseInt(localStorage.getItem('uploadStartTime'));
            
            if (fileName && startTime) {
                this.uploadStartTime = startTime;
                this.showNotification(fileName);
                this.startProgressSimulation();
            }
        }
    }
}

// Crear una instancia global del manejador
window.uploadHandler = new UploadHandler(); 