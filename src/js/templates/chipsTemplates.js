import { baseTemplate } from './base.js';

export const listarChipsTemplate = (chips = []) => `
    <div class="page-container">
        <h1>Gestão de Chips</h1>
        <div class="actions-container">
            <button onclick="window.location.href='/chips/adicionar'" class="btn-primary">Novo Chip</button>
            <button onclick="window.location.href='/chips/importar'" class="btn-secondary">Importar</button>
            <button onclick="window.location.href='/chips/modelo'" class="btn-secondary">Download Modelo CSV</button>
        </div>
        
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Número</th>
                        <th>Funcionário</th>
                        <th>Centro de Custo</th>
                        <th>Função</th>
                        <th>Valor</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${chips.map(chip => `
                        <tr>
                            <td>${chip.numero}</td>
                            <td>${chip.funcionario_nome || '-'}</td>
                            <td>${chip.centro_custo || '-'}</td>
                            <td>${chip.funcao || '-'}</td>
                            <td>R$ ${chip.valor ? parseFloat(chip.valor).toFixed(2) : '0.00'}</td>
                            <td>${chip.status}</td>
                            <td class="actions">
                                <button onclick="window.location.href='/chips/${chip.id}/editar'" class="btn-edit">Editar</button>
                                <button onclick="excluirChip(${chip.id})" class="btn-delete">Excluir</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>
`;

export const adicionarChipTemplate = (centros_custo = []) => `
    <div class="page-container">
        <h1>Adicionar Chip</h1>
        <form id="formChip" class="form-container">
            <div class="form-group">
                <label for="numero">Número</label>
                <input type="text" id="numero" name="numero" required pattern="[0-9]{10,11}">
            </div>
            
            <div class="form-group">
                <label for="funcionario_nome">Funcionário</label>
                <input type="text" id="funcionario_nome" name="funcionario_nome">
            </div>
            
            <div class="form-group">
                <label for="centro_custo_id">Centro de Custo</label>
                <select id="centro_custo_id" name="centro_custo_id" required>
                    <option value="">Selecione um centro de custo</option>
                    ${centros_custo.map(cc => `
                        <option value="${cc.id}">${cc.nome}</option>
                    `).join('')}
                </select>
            </div>
            
            <div class="form-group">
                <label for="funcao">Função</label>
                <input type="text" id="funcao" name="funcao">
            </div>
            
            <div class="form-group">
                <label for="valor">Valor</label>
                <input type="number" id="valor" name="valor" step="0.01">
            </div>
            
            <div class="form-group">
                <label for="vencimento_fatura">Dia de Vencimento</label>
                <input type="number" id="vencimento_fatura" name="vencimento_fatura" min="1" max="31">
            </div>
            
            <div class="form-group">
                <label for="status">Status</label>
                <select id="status" name="status" required>
                    <option value="Ativo">Ativo</option>
                    <option value="Inativo">Inativo</option>
                    <option value="Cancelado">Cancelado</option>
                </select>
            </div>
            
            <button type="submit" class="btn-submit">Adicionar</button>
            <a href="/chips" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const importarChipsTemplate = () => `
    <div class="page-container">
        <h1>Importar Chips</h1>
        <form id="formImportarChips" class="form-container">
            <div class="form-group">
                <label for="arquivo">Arquivo CSV</label>
                <input type="file" id="arquivo" name="arquivo" accept=".csv" required>
            </div>
            
            <div class="info-box">
                <h3>Formato do arquivo CSV:</h3>
                <p>O arquivo deve conter as seguintes colunas:</p>
                <ul>
                    <li>Numero (obrigatório)</li>
                    <li>Funcionario Nome</li>
                    <li>Centro de Custo</li>
                    <li>Funcao</li>
                    <li>Valor</li>
                    <li>Vencimento Fatura</li>
                    <li>Status</li>
                </ul>
            </div>
            
            <button type="submit" class="btn-submit">Importar</button>
            <a href="/chips" class="btn-link">Voltar</a>
        </form>
    </div>
`;