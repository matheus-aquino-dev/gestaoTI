import { notifications } from './notifications.js';
import { validateForm } from './validation.js';

class FormHandlers {
    constructor() {
        this.setupGlobalHandlers();
    }

    setupGlobalHandlers() {
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (form.id) {
                e.preventDefault();
                this[form.id]?.(e);
            }
        });
    }

    async formLogin(e) {
        const form = e.target;
        const data = new FormData(form);
        
        const rules = {
            email: ['required', 'email'],
            senha: ['required', 'minLength:6']
        };

        const validation = validateForm(Object.fromEntries(data), rules);
        
        if (!validation.isValid) {
            notifications.error(Object.values(validation.errors)[0]);
            return;
        }

        try {
            // Implementar autenticação
            notifications.success('Login realizado com sucesso!');
            window.location.href = '/';
        } catch (error) {
            notifications.error('Erro ao fazer login: ' + error.message);
        }
    }

    async formRegister(e) {
        const form = e.target;
        const data = new FormData(form);
        
        const rules = {
            nome: ['required'],
            email: ['required', 'email'],
            senha: ['required', 'minLength:6'],
            confirmarSenha: ['required']
        };

        const validation = validateForm(Object.fromEntries(data), rules);
        
        if (!validation.isValid) {
            notifications.error(Object.values(validation.errors)[0]);
            return;
        }

        if (data.get('senha') !== data.get('confirmarSenha')) {
            notifications.error('As senhas não coincidem');
            return;
        }

        try {
            // Implementar registro
            notifications.success('Registro realizado com sucesso!');
            window.location.href = '/login';
        } catch (error) {
            notifications.error('Erro ao registrar: ' + error.message);
        }
    }

    async formCategoria(e) {
        const form = e.target;
        const data = new FormData(form);
        
        const rules = {
            nome: ['required']
        };

        const validation = validateForm(Object.fromEntries(data), rules);
        
        if (!validation.isValid) {
            notifications.error(Object.values(validation.errors)[0]);
            return;
        }

        try {
            // Implementar criação de categoria
            notifications.success('Categoria criada com sucesso!');
            window.location.href = '/categorias';
        } catch (error) {
            notifications.error('Erro ao criar categoria: ' + error.message);
        }
    }

    async formAtivo(e) {
        const form = e.target;
        const data = new FormData(form);
        
        const rules = {
            nome: ['required'],
            categoria: ['required'],
            status: ['required']
        };

        const validation = validateForm(Object.fromEntries(data), rules);
        
        if (!validation.isValid) {
            notifications.error(Object.values(validation.errors)[0]);
            return;
        }

        try {
            // Implementar criação de ativo
            notifications.success('Ativo criado com sucesso!');
            window.location.href = '/ativos';
        } catch (error) {
            notifications.error('Erro ao criar ativo: ' + error.message);
        }
    }

    async formDemanda(e) {
        const form = e.target;
        const data = new FormData(form);
        
        const rules = {
            titulo: ['required'],
            descricao: ['required'],
            prioridade: ['required'],
            prazo: ['required', 'date']
        };

        const validation = validateForm(Object.fromEntries(data), rules);
        
        if (!validation.isValid) {
            notifications.error(Object.values(validation.errors)[0]);
            return;
        }

        try {
            // Implementar criação de demanda
            notifications.success('Demanda criada com sucesso!');
            window.location.href = '/demandas';
        } catch (error) {
            notifications.error('Erro ao criar demanda: ' + error.message);
        }
    }
}

export const formHandlers = new FormHandlers();