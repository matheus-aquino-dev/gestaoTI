import { baseTemplate } from './base.js';
import { notifications } from '../utils/notifications.js';

export const adicionarAtivoTemplate = (categorias) => `
    <div class="page-container">
        <h1>Adicionar Ativo</h1>
        <form id="formAtivo" class="form-container">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" name="nome" id="nome" required>
            </div>
            <div class="form-group">
                <label for="categoria">Categoria:</label>
                <select name="categoria" id="categoria" required>
                    <option value="">Selecione uma categoria</option>
                    ${categorias.map(cat => `
                        <option value="${cat.id}">${cat.nome}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="status">Status:</label>
                <select name="status" id="status" required>
                    <option value="disponivel">Disponível</option>
                    <option value="em_uso">Em uso</option>
                    <option value="manutencao">Manutenção</option>
                </select>
            </div>
            <input type="submit" value="Adicionar" class="btn-submit">
            <a href="/" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const listarAtivosTemplate = (ativos = []) => `
    <div class="page-container">
        <h1>Gestão de Ativos</h1>
        <div class="actions-container">
            <button onclick="window.location.href='/ativo/adicionar'" class="btn-primary">Novo Ativo</button>
            <button onclick="window.location.href='/importar'" class="btn-secondary">Importar CSV</button>
            <button onclick="window.location.href='/exportar/pdf'" class="btn-secondary">Exportar PDF</button>
            <button onclick="window.location.href='/exportar/excel'" class="btn-secondary">Exportar Excel</button>
        </div>
        
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Categoria</th>
                        <th>Centro de Custo</th>
                        <th>Status</th>
                        <th>Responsável</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${ativos.map(ativo => `
                        <tr>
                            <td>${ativo.nome}</td>
                            <td>${ativo.categoria || '-'}</td>
                            <td>${ativo.centro_custo || '-'}</td>
                            <td>${ativo.status}</td>
                            <td>${ativo.funcionario_nome || '-'}</td>
                            <td class="actions">
                                <button onclick="window.location.href='/ativo/${ativo.id}'" class="btn-view">Ver</button>
                                <button onclick="window.location.href='/ativo/${ativo.id}/editar'" class="btn-edit">Editar</button>
                                <button onclick="excluirAtivo(${ativo.id})" class="btn-delete">Excluir</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>
`;

export const editarAtivoTemplate = (ativo, categorias = [], centros_custo = []) => `
    <div class="page-container">
        <h1>Editar Ativo</h1>
        <form id="formEditarAtivo" class="form-container">
            <input type="hidden" name="id" value="${ativo.id}">
            
            <div class="form-group">
                <label for="nome">Nome</label>
                <input type="text" id="nome" name="nome" value="${ativo.nome}" required>
            </div>
            
            <div class="form-group">
                <label for="categoria_id">Categoria</label>
                <select id="categoria_id" name="categoria_id" required>
                    <option value="">Selecione uma categoria</option>
                    ${categorias.map(cat => `
                        <option value="${cat.id}" ${cat.id === ativo.categoria_id ? 'selected' : ''}>
                            ${cat.nome}
                        </option>
                    `).join('')}
                </select>
            </div>
            
            <div class="form-group">
                <label for="centro_custo_id">Centro de Custo</label>
                <select id="centro_custo_id" name="centro_custo_id" required>
                    <option value="">Selecione um centro de custo</option>
                    ${centros_custo.map(cc => `
                        <option value="${cc.id}" ${cc.id === ativo.centro_custo_id ? 'selected' : ''}>
                            ${cc.nome}
                        </option>
                    `).join('')}
                </select>
            </div>
            
            <div class="form-group">
                <label for="modelo">Modelo</label>
                <input type="text" id="modelo" name="modelo" value="${ativo.modelo || ''}">
            </div>
            
            <div class="form-group">
                <label for="valor">Valor</label>
                <input type="number" id="valor" name="valor" step="0.01" value="${ativo.valor || ''}">
            </div>
            
            <div class="form-group">
                <label for="numero_serie">Número de Série</label>
                <input type="text" id="numero_serie" name="numero_serie" value="${ativo.numero_serie || ''}">
            </div>
            
            <div class="form-group">
                <label for="patrimonio">Patrimônio</label>
                <input type="text" id="patrimonio" name="patrimonio" value="${ativo.patrimonio || ''}">
            </div>
            
            <div class="form-group">
                <label for="data_aquisicao">Data de Aquisição</label>
                <input type="date" id="data_aquisicao" name="data_aquisicao" value="${ativo.data_aquisicao || ''}">
            </div>
            
            <div class="form-group">
                <label for="descricao">Descrição</label>
                <textarea id="descricao" name="descricao" rows="3">${ativo.descricao || ''}</textarea>
            </div>
            
            <button type="submit" class="btn-submit">Salvar</button>
            <a href="/" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const detalhesAtivoTemplate = (ativo, historico = [], alocacao = null) => `
    <div class="page-container">
        <h1>Detalhes do Ativo</h1>
        
        <div class="details-container">
            <div class="detail-item">
                <span class="label">Nome:</span>
                <span class="value">${ativo.nome}</span>
            </div>
            
            <div class="detail-item">
                <span class="label">Categoria:</span>
                <span class="value">${ativo.categoria || '-'}</span>
            </div>
            
            <div class="detail-item">
                <span class="label">Centro de Custo:</span>
                <span class="value">${ativo.centro_custo || '-'}</span>
            </div>
            
            <div class="detail-item">
                <span class="label">Status:</span>
                <span class="value">${ativo.status}</span>
            </div>
            
            ${alocacao ? `
                <div class="detail-item">
                    <span class="label">Responsável:</span>
                    <span class="value">${alocacao.funcionario_nome}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Data de Alocação:</span>
                    <span class="value">${new Date(alocacao.data_alocacao).toLocaleDateString()}</span>
                </div>
            ` : ''}
        </div>
        
        <div class="actions-container">
            <button onclick="window.location.href='/ativo/${ativo.id}/editar'" class="btn-edit">Editar</button>
            ${!alocacao ? `
                <button onclick="showAlocarModal(${ativo.id})" class="btn-primary">Alocar</button>
            ` : `
                <button onclick="devolverAtivo(${ativo.id})" class="btn-secondary">Devolver</button>
            `}
            <a href="/" class="btn-link">Voltar</a>
        </div>
        
        ${historico.length > 0 ? `
            <div class="history-container">
                <h2>Histórico de Alocações</h2>
                <div class="timeline">
                    ${historico.map(h => `
                        <div class="timeline-item">
                            <div class="timeline-date">
                                ${new Date(h.data_alocacao).toLocaleDateString()}
                            </div>
                            <div class="timeline-content">
                                <p>Alocado para: ${h.funcionario_nome}</p>
                                ${h.data_devolucao ? `
                                    <p>Devolvido em: ${new Date(h.data_devolucao).toLocaleDateString()}</p>
                                ` : ''}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
    </div>
`;