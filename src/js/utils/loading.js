export class LoadingManager {
    constructor() {
        this.createLoadingElement();
    }

    createLoadingElement() {
        this.loadingElement = document.createElement('div');
        this.loadingElement.className = 'loading-overlay';
        this.loadingElement.innerHTML = `
            <div class="loading-spinner"></div>
            <div class="loading-text">Carregando...</div>
        `;
        document.body.appendChild(this.loadingElement);
    }

    show(message = 'Carregando...') {
        this.loadingElement.querySelector('.loading-text').textContent = message;
        this.loadingElement.classList.add('active');
        document.body.classList.add('loading');
    }

    hide() {
        this.loadingElement.classList.remove('active');
        document.body.classList.remove('loading');
    }

    async withLoading(promise, message = 'Carregando...') {
        try {
            this.show(message);
            return await promise;
        } finally {
            this.hide();
        }
    }
}

export const loading = new LoadingManager();