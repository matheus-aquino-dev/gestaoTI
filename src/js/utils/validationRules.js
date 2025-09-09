export const validationRules = {
    ativo: {
        nome: {
            required: true,
            minLength: 3,
            message: 'Nome do ativo deve ter pelo menos 3 caracteres'
        },
        categoria: {
            required: true,
            message: 'Categoria é obrigatória'
        },
        status: {
            required: true,
            enum: ['disponivel', 'em_uso', 'manutencao'],
            message: 'Status inválido'
        }
    },
    
    demanda: {
        titulo: {
            required: true,
            minLength: 5,
            message: 'Título deve ter pelo menos 5 caracteres'
        },
        descricao: {
            required: true,
            minLength: 10,
            message: 'Descrição deve ter pelo menos 10 caracteres'
        },
        prioridade: {
            required: true,
            enum: ['baixa', 'media', 'alta'],
            message: 'Prioridade inválida'
        },
        prazo: {
            required: true,
            futureDate: true,
            message: 'Prazo deve ser uma data futura'
        }
    },
    
    usuario: {
        nome: {
            required: true,
            minLength: 3,
            message: 'Nome deve ter pelo menos 3 caracteres'
        },
        email: {
            required: true,
            email: true,
            message: 'Email inválido'
        },
        senha: {
            required: true,
            minLength: 6,
            pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/,
            message: 'Senha deve ter pelo menos 6 caracteres, uma letra e um número'
        }
    },
    
    categoria: {
        nome: {
            required: true,
            minLength: 2,
            message: 'Nome da categoria deve ter pelo menos 2 caracteres'
        }
    }
};