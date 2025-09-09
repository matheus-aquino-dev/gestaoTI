import { baseTemplate } from './base.js';

export const adicionarCategoriaTemplate = () => `
    <div class="page-container">
        <h1>Adicionar Categoria</h1>
        <form id="formCategoria" class="form-container">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" name="nome" id="nome" required>
            </div>
            <input type="submit" value="Adicionar" class="btn-submit">
            <a href="/" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const editarCategoriaTemplate = (categoria) => `
    <div class="page-container">
        <h1>Editar Categoria</h1>
        <form id="formEditarCategoria" class="form-container">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" name="nome" id="nome" value="${categoria.nome}" required>
            </div>
            <input type="submit" value="Salvar" class="btn-submit">
            <a href="/" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const listarCategoriasTemplate = (categorias) => `
    <div class="page-container">
        <h1>Categorias</h1>
        <div class="actions-container">
            <button onclick="window.location.href='/adicionar-categoria'" class="btn-primary">Nova Categoria</button>
        </div>
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${categorias.map(cat => `
                        <tr>
                            <td>${cat.nome}</td>
                            <td class="actions">
                                <button onclick="editarCategoria('${cat.id}')" class="btn-edit">Editar</button>
                                <button onclick="excluirCategoria('${cat.id}')" class="btn-delete">Excluir</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>
`;