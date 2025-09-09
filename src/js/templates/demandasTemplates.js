import { baseTemplate } from './base.js';

export const listarDemandasTemplate = (abertas = [], andamento = [], concluidas = []) => `
    <div class="page-container">
        <h1>Gestão de Demandas</h1>
        <div class="actions-container">
            <button onclick="window.location.href='/demandas/adicionar'" class="btn-primary">Nova Demanda</button>
        </div>
        
        <div class="demands-grid">
            <div class="demands-column">
                <h2>Abertas</h2>
                ${renderDemandasList(abertas)}
            </div>
            
            <div class="demands-column">
                <h2>Em Andamento</h2>
                ${renderDemandasList(andamento)}
            </div>
            
            <div class="demands-column">
                <h2>Concluídas</h2>
                ${renderDemandasList(concluidas)}
            </div>
        </div>
    </div>
`;

export const adicionarDemandaTemplate = () => `
    <div class="page-container">
        <h1>Nova Demanda</h1>
        <form id="formDemanda" class="form-container">
            <div class="form-group">
                <label for="nome_solicitante">Nome do Solicitante</label>
                <input type="text" id="nome_solicitante" name="nome_solicitante" required>
            </div>
            
            <div class="form-group">
                <label for="departamento">Departamento</label>
                <select id="departamento" name="departamento" required>
                    <option value="">Selecione um departamento</option>
                    <option value="TI">TI</option>
                    <option value="RH">RH</option>
                    <option value="Financeiro">Financeiro</option>
                    <option value="Comercial">Comercial</option>
                    <option value="Operacional">Operacional</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="urgencia">Urgência</label>
                <select id="urgencia" name="urgencia" required>
                    <option value="Baixa">Baixa</option>
                    <option value="Média">Média</option>
                    <option value="Alta">Alta</option>
                    <option value="Crítica">Crítica</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="descricao">Descrição</label>
                <textarea id="descricao" name="descricao" rows="4" required></textarea>
            </div>
            
            <button type="submit" class="btn-submit">Criar Demanda</button>
            <a href="/demandas" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const detalhesDemandaTemplate = (demanda, historico = []) => `
    <div class="page-container">
        <h1>Detalhes da Demanda</h1>
        
        <div class="details-container">
            <div class="detail-item">
                <span class="label">Solicitante:</span>
                <span class="value">${demanda.nome_solicitante}</span>
            </div>
            
            <div class="detail-item">
                <span class="label">Departamento:</span>
                <span class="value">${demanda.departamento}</span>
            </div>
            
            <div class="detail-item">
                <span class="label">Urgência:</span>
                <span class="value">${demanda.urgencia}</span>
            </div>
            
            <div class="detail-item">
                <span class="label">Status:</span>
                <span class="value">${demanda.status}</span>
            </div>
            
            <div class="detail-item">
                <span class="label">Data de Criação:</span>
                <span class="value">${new Date(demanda.data_criacao).toLocaleDateString()}</span>
            </div>
            
            ${demanda.responsavel ? `
                <div class="detail-item">
                    <span class="label">Responsável:</span>
                    <span class="value">${demanda.responsavel}</span>
                </div>
            ` : ''}
            
            ${demanda.data_conclusao ? `
                <div class="detail-item">
                    <span class="label">Data de Conclusão:</span>
                    <span class="value">${new Date(demanda.data_conclusao).toLocaleDateString()}</span>
                </div>
            ` : ''}
            
            <div class="detail-item full-width">
                <span class="label">Descrição:</span>
                <div class="value description">${demanda.descricao}</div>
            </div>
        </div>
        
        <div class="actions-container">
            ${demanda.status === 'Aberta' ? `
                <button onclick="assumirDemanda(${demanda.id})" class="btn-primary">Assumir Demanda</button>
            ` : ''}
            
            ${demanda.status === 'Em Andamento' ? `
                <button onclick="concluirDemanda(${demanda.id})" class="btn-success">Concluir Demanda</button>
            ` : ''}
            
            <a href="/demandas" class="btn-link">Voltar</a>
        </div>
        
        ${historico.length > 0 ? `
            <div class="history-container">
                <h2>Histórico</h2>
                <div class="timeline">
                    ${historico.map(h => `
                        <div class="timeline-item">
                            <div class="timeline-date">
                                ${new Date(h.data).toLocaleString()}
                            </div>
                            <div class="timeline-content">
                                <p>${h.alteracao}</p>
                                <small>Por: ${h.autor}</small>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
    </div>
`;

function renderDemandasList(demandas) {
    if (demandas.length === 0) {
        return '<div class="empty-state">Nenhuma demanda</div>';
    }
    
    return `
        <div class="demands-list">
            ${demandas.map(demanda => `
                <div class="demand-card">
                    <div class="demand-header">
                        <span class="demand-urgency ${demanda.urgencia.toLowerCase()}">${demanda.urgencia}</span>
                        <span class="demand-date">${new Date(demanda.data_criacao).toLocaleDateString()}</span>
                    </div>
                    <div class="demand-body">
                        <h3>${demanda.nome_solicitante}</h3>
                        <p>${demanda.departamento}</p>
                        <div class="demand-description">${demanda.descricao.substring(0, 100)}...</div>
                    </div>
                    <div class="demand-footer">
                        <button onclick="window.location.href='/demandas/${demanda.id}'" class="btn-view">
                            Ver Detalhes
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}