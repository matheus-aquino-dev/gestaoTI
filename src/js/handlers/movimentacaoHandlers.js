import { CrudHandlers } from './crudHandlers.js';
import { loading } from '../utils/loading.js';
import { notifications } from '../utils/notifications.js';

export class ChipHandlers extends CrudHandlers {
    constructor() {
        super('Chip', 'chip');
    }

    async importarChips(arquivo) {
        return await loading.withLoading(
            (async () => {
                try {
                    const reader = new FileReader();
                    const texto = await new Promise((resolve) => {
                        reader.onload = (e) => resolve(e.target.result);
                        reader.readAsText(arquivo);
                    });

                    const linhas = texto.split('\n');
                    const cabecalho = linhas[0].split(',');
                    const chips = linhas.slice(1).map(linha => {
                        const valores = linha.split(',');
                        const chip = {};
                        cabecalho.forEach((coluna, index) => {
                            chip[coluna.trim()] = valores[index]?.trim();
                        });
                        return chip;
                    });

                    // Implementar importação quando integrar com Firebase
                    notifications.success('Chips importados com sucesso!');
                    return chips;
                } catch (error) {
                    notifications.error('Erro ao importar chips: ' + error.message);
                    throw error;
                }
            })(),
            'Importando chips...'
        );
    }
}

export class MovimentacaoHandlers {
    async alocarAtivo(dados) {
        return await loading.withLoading(
            (async () => {
                try {
                    // Implementar alocação quando integrar com Firebase
                    notifications.success('Ativo alocado com sucesso!');
                } catch (error) {
                    notifications.error('Erro ao alocar ativo: ' + error.message);
                    throw error;
                }
            })(),
            'Alocando ativo...'
        );
    }

    async devolverAtivo(dados) {
        return await loading.withLoading(
            (async () => {
                try {
                    // Implementar devolução quando integrar com Firebase
                    notifications.success('Ativo devolvido com sucesso!');
                } catch (error) {
                    notifications.error('Erro ao devolver ativo: ' + error.message);
                    throw error;
                }
            })(),
            'Devolvendo ativo...'
        );
    }

    async obterHistoricoAtivo(ativoId) {
        return await loading.withLoading(
            (async () => {
                try {
                    // Implementar consulta quando integrar com Firebase
                    return [];
                } catch (error) {
                    notifications.error('Erro ao obter histórico: ' + error.message);
                    throw error;
                }
            })(),
            'Carregando histórico...'
        );
    }
}