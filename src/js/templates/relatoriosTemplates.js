import { baseTemplate } from './base.js';

export const historicoAtivoTemplate = (historico, ativo) => `
    <div class="page-container">
        <h1>Histórico do Ativo</h1>
        <div class="details-container">
            <h2>${ativo.nome}</h2>
            <div class="detail-item">
                <span class="label">Categoria:</span>
                <span class="value">${ativo.categoria}</span>
            </div>
        </div>
        <div class="timeline">
            ${historico.map(evento => `
                <div class="timeline-item">
                    <div class="timeline-date">${new Date(evento.data).toLocaleDateString()}</div>
                    <div class="timeline-content">
                        <h3>${evento.tipo}</h3>
                        <p>${evento.descricao}</p>
                        <div class="timeline-meta">
                            <span>Responsável: ${evento.responsavel}</span>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
        <div class="actions-container">
            <a href="/ativos" class="btn-link">Voltar</a>
        </div>
    </div>
`;

export const previewImportacaoTemplate = (dados) => `
    <div class="page-container">
        <h1>Preview da Importação</h1>
        <div class="preview-container">
            <div class="preview-summary">
                <h3>Resumo</h3>
                <p>Total de registros: ${dados.length}</p>
            </div>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            ${Object.keys(dados[0] || {}).map(key => `
                                <th>${key}</th>
                            `).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${dados.map(item => `
                            <tr>
                                ${Object.values(item).map(value => `
                                    <td>${value}</td>
                                `).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="actions-container">
            <button onclick="confirmarImportacao()" class="btn-primary">Confirmar Importação</button>
            <a href="/chips" class="btn-link">Cancelar</a>
        </div>
    </div>
`;

export const relatoriosTemplate = () => `
    <div class="page-container">
        <h1>Relatórios</h1>
        <div class="reports-grid">
            <div class="report-card" onclick="gerarRelatorio('ativos')">
                <h3>Inventário de Ativos</h3>
                <p>Lista completa de ativos e seus status</p>
            </div>
            <div class="report-card" onclick="gerarRelatorio('alocacoes')">
                <h3>Alocações Ativas</h3>
                <p>Ativos atualmente alocados e seus responsáveis</p>
            </div>
            <div class="report-card" onclick="gerarRelatorio('movimentacoes')">
                <h3>Movimentações</h3>
                <p>Histórico de movimentações por período</p>
            </div>
            <div class="report-card" onclick="gerarRelatorio('chips')">
                <h3>Controle de Chips</h3>
                <p>Situação atual dos chips e linhas</p>
            </div>
        </div>
    </div>
`;