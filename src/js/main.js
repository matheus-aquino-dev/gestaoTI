import { loginTemplate, registerTemplate } from './templates/authTemplates.js';
import { listarAtivosTemplate } from './templates/ativosTemplates.js';
import { notifications } from './utils/notifications.js';

class App {
    constructor() {
        this.app = document.getElementById('app');
        this.isAuthenticated = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthAndRender();
    }

    checkAuthAndRender() {
        if (!this.isAuthenticated) {
            this.renderPage(loginTemplate());
        } else {
            this.renderPage(listarAtivosTemplate(mockData.ativos));
        }
    }

    renderPage(template) {
        this.app.innerHTML = template;
    }

    setupEventListeners() {
        document.addEventListener('submit', (e) => {
            if (e.target.id === 'formLogin') {
                e.preventDefault();
                this.handleLogin(e);
            }
        });

        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href]')) {
                e.preventDefault();
                const href = e.target.getAttribute('href');
                this.handleNavigation(href);
            }
        });
    }

    handleLogin(e) {
        const form = e.target;
        const email = form.querySelector('#email').value;
        const senha = form.querySelector('#senha').value;

        if (email && senha) {
            this.isAuthenticated = true;
            notifications.success('Login realizado com sucesso!');
            this.renderPage(listarAtivosTemplate(mockData.ativos));
        } else {
            notifications.error('Email e senha são obrigatórios');
        }
    }

    handleNavigation(path) {
        switch(path) {
            case '/':
                this.checkAuthAndRender();
                break;
            case '/login':
                this.renderPage(loginTemplate());
                break;
            case '/register':
                this.renderPage(registerTemplate());
                break;
            case '/logout':
                this.isAuthenticated = false;
                localStorage.removeItem('token');
                this.renderPage(loginTemplate());
                break;
            default:
                if (!this.isAuthenticated) {
                    this.renderPage(loginTemplate());
                    notifications.error('Por favor, faça login para continuar');
                } else {
                    notifications.info('Página em construção');
                }
        }
    }
}

// Inicializa a aplicação
new App();