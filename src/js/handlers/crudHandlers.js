import { loading } from '../utils/loading.js';
import { notifications } from '../utils/notifications.js';
import { validationRules } from '../utils/validationRules.js';
import router from '../router.js';

export class CrudHandlers {
    constructor(entityName, validationKey) {
        this.entityName = entityName;
        this.validationRules = validationRules[validationKey];
    }

    async handleCreate(data) {
        return await loading.withLoading(
            (async () => {
                try {
                    // Implementar criação quando integrar com Firebase
                    notifications.success(`${this.entityName} criado com sucesso!`);
                    router.navigate(`/${this.entityName.toLowerCase()}s`);
                } catch (error) {
                    notifications.error(`Erro ao criar ${this.entityName}: ${error.message}`);
                    throw error;
                }
            })(),
            `Criando ${this.entityName}...`
        );
    }

    async handleUpdate(id, data) {
        return await loading.withLoading(
            (async () => {
                try {
                    // Implementar atualização quando integrar com Firebase
                    notifications.success(`${this.entityName} atualizado com sucesso!`);
                    router.navigate(`/${this.entityName.toLowerCase()}s`);
                } catch (error) {
                    notifications.error(`Erro ao atualizar ${this.entityName}: ${error.message}`);
                    throw error;
                }
            })(),
            `Atualizando ${this.entityName}...`
        );
    }

    async handleDelete(id) {
        if (!confirm(`Deseja realmente excluir este ${this.entityName}?`)) {
            return;
        }

        return await loading.withLoading(
            (async () => {
                try {
                    // Implementar exclusão quando integrar com Firebase
                    notifications.success(`${this.entityName} excluído com sucesso!`);
                    router.navigate(`/${this.entityName.toLowerCase()}s`);
                } catch (error) {
                    notifications.error(`Erro ao excluir ${this.entityName}: ${error.message}`);
                    throw error;
                }
            })(),
            `Excluindo ${this.entityName}...`
        );
    }

    async handleList() {
        return await loading.withLoading(
            (async () => {
                try {
                    // Implementar listagem quando integrar com Firebase
                    return [];
                } catch (error) {
                    notifications.error(`Erro ao listar ${this.entityName}s: ${error.message}`);
                    throw error;
                }
            })(),
            `Carregando ${this.entityName}s...`
        );
    }

    validate(data) {
        const errors = {};
        
        for (const [field, rules] of Object.entries(this.validationRules)) {
            if (rules.required && !data[field]) {
                errors[field] = rules.message || 'Campo obrigatório';
                continue;
            }

            if (rules.minLength && data[field]?.length < rules.minLength) {
                errors[field] = rules.message || `Mínimo de ${rules.minLength} caracteres`;
                continue;
            }

            if (rules.pattern && !rules.pattern.test(data[field])) {
                errors[field] = rules.message || 'Formato inválido';
                continue;
            }

            if (rules.enum && !rules.enum.includes(data[field])) {
                errors[field] = rules.message || 'Valor inválido';
                continue;
            }

            if (rules.futureDate && new Date(data[field]) <= new Date()) {
                errors[field] = rules.message || 'Data deve ser futura';
                continue;
            }
        }

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }
}