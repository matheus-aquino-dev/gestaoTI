import { notifications } from '../utils/notifications.js';
import { loading } from '../utils/loading.js';
import router from '../router.js';

class AuthHandler {
    async register(formData) {
        return await loading.withLoading(
            (async () => {
                try {
                    const response = await fetch('/api/auth/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            nome: formData.get('nome'),
                            email: formData.get('email'),
                            departamento: formData.get('departamento'),
                            senha: formData.get('senha')
                        })
                    });

                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.message || 'Erro no registro');
                    }

                    notifications.success('Registro realizado com sucesso!');
                    router.navigate('/login');
                } catch (error) {
                    notifications.error(error.message);
                    throw error;
                }
            })(),
            'Registrando usuário...'
        );
    }

    validateRegisterData(formData) {
        const senha = formData.get('senha');
        const confirmarSenha = formData.get('confirmarSenha');

        if (senha !== confirmarSenha) {
            throw new Error('As senhas não coincidem');
        }

        if (senha.length < 6) {
            throw new Error('A senha deve ter pelo menos 6 caracteres');
        }

        if (!formData.get('email').includes('@')) {
            throw new Error('Email inválido');
        }

        return true;
    }

    setupEventListeners() {
        document.addEventListener('submit', async (e) => {
            if (e.target.id === 'registerForm') {
                e.preventDefault();
                const formData = new FormData(e.target);
                
                try {
                    this.validateRegisterData(formData);
                    await this.register(formData);
                } catch (error) {
                    notifications.error(error.message);
                }
            }
        });
    }
}

export const authHandler = new AuthHandler();