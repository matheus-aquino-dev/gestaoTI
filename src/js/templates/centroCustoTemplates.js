import { baseTemplate } from './base.js';

export const listarCentroCustoTemplate = (centrosCusto) => `
    <div class="page-container">
        <h1>Centros de Custo</h1>
        <div class="actions-container">
            <button onclick="window.location.href='/adicionar-centro-custo'" class="btn-primary">Novo Centro de Custo</button>
        </div>
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Nome</th>
                        <th>Responsável</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${centrosCusto.map(centro => `
                        <tr>
                            <td>${centro.codigo}</td>
                            <td>${centro.nome}</td>
                            <td>${centro.responsavel}</td>
                            <td class="actions">
                                <button onclick="editarCentroCusto('${centro.id}')" class="btn-edit">Editar</button>
                                <button onclick="excluirCentroCusto('${centro.id}')" class="btn-delete">Excluir</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>
`;

export const adicionarCentroCustoTemplate = () => `
    <div class="page-container">
        <h1>Novo Centro de Custo</h1>
        <form id="formCentroCusto" class="form-container">
            <div class="form-group">
                <label for="codigo">Código:</label>
                <input type="text" id="codigo" name="codigo" required>
            </div>
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required>
            </div>
            <div class="form-group">
                <label for="responsavel">Responsável:</label>
                <input type="text" id="responsavel" name="responsavel" required>
            </div>
            <div class="form-group">
                <label for="descricao">Descrição:</label>
                <textarea id="descricao" name="descricao" rows="3"></textarea>
            </div>
            <input type="submit" value="Criar" class="btn-submit">
            <a href="/centro-custo" class="btn-link">Voltar</a>
        </form>
    </div>
`;