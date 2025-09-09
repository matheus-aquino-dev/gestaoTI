import { baseTemplate } from './base.js';

export const alocarAtivoTemplate = (ativo, usuarios) => `
    <div class="page-container">
        <h1>Alocar Ativo</h1>
        <div class="details-container">
            <h2>Detalhes do Ativo</h2>
            <div class="detail-item">
                <span class="label">Nome:</span>
                <span class="value">${ativo.nome}</span>
            </div>
            <div class="detail-item">
                <span class="label">Categoria:</span>
                <span class="value">${ativo.categoria}</span>
            </div>
        </div>
        <form id="formAlocarAtivo" class="form-container">
            <input type="hidden" name="ativoId" value="${ativo.id}">
            <div class="form-group">
                <label for="usuario">Usuário:</label>
                <select id="usuario" name="usuario" required>
                    <option value="">Selecione um usuário</option>
                    ${usuarios.map(user => `
                        <option value="${user.id}">${user.nome}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="dataAlocacao">Data de Alocação:</label>
                <input type="date" id="dataAlocacao" name="dataAlocacao" required value="${new Date().toISOString().split('T')[0]}">
            </div>
            <div class="form-group">
                <label for="observacao">Observação:</label>
                <textarea id="observacao" name="observacao" rows="3"></textarea>
            </div>
            <input type="submit" value="Alocar" class="btn-submit">
            <a href="/ativos" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const devolverAtivoTemplate = (ativo) => `
    <div class="page-container">
        <h1>Devolver Ativo</h1>
        <div class="details-container">
            <h2>Detalhes do Ativo</h2>
            <div class="detail-item">
                <span class="label">Nome:</span>
                <span class="value">${ativo.nome}</span>
            </div>
            <div class="detail-item">
                <span class="label">Categoria:</span>
                <span class="value">${ativo.categoria}</span>
            </div>
            <div class="detail-item">
                <span class="label">Responsável:</span>
                <span class="value">${ativo.responsavel}</span>
            </div>
            <div class="detail-item">
                <span class="label">Data de Alocação:</span>
                <span class="value">${new Date(ativo.dataAlocacao).toLocaleDateString()}</span>
            </div>
        </div>
        <form id="formDevolverAtivo" class="form-container">
            <input type="hidden" name="ativoId" value="${ativo.id}">
            <div class="form-group">
                <label for="dataDevolucao">Data de Devolução:</label>
                <input type="date" id="dataDevolucao" name="dataDevolucao" required value="${new Date().toISOString().split('T')[0]}">
            </div>
            <div class="form-group">
                <label for="estado">Estado do Ativo:</label>
                <select id="estado" name="estado" required>
                    <option value="bom">Bom</option>
                    <option value="regular">Regular</option>
                    <option value="ruim">Ruim</option>
                </select>
            </div>
            <div class="form-group">
                <label for="observacao">Observação:</label>
                <textarea id="observacao" name="observacao" rows="3"></textarea>
            </div>
            <input type="submit" value="Devolver" class="btn-submit">
            <a href="/ativos" class="btn-link">Voltar</a>
        </form>
    </div>
`;