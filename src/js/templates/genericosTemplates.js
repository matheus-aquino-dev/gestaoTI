import { baseTemplate } from './base.js';

export const listarGenericosTemplate = (genericos) => `
    <div class="page-container">
        <h1>Ativos Genéricos</h1>
        <div class="actions-container">
            <button onclick="window.location.href='/adicionar-generico'" class="btn-primary">Novo Ativo Genérico</button>
            <button onclick="window.location.href='/importar-simples'" class="btn-secondary">Importar</button>
        </div>
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Quantidade</th>
                        <th>Localização</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${genericos.map(item => `
                        <tr>
                            <td>${item.nome}</td>
                            <td>${item.quantidade}</td>
                            <td>${item.localizacao}</td>
                            <td>${item.status}</td>
                            <td class="actions">
                                <button onclick="editarGenerico('${item.id}')" class="btn-edit">Editar</button>
                                <button onclick="excluirGenerico('${item.id}')" class="btn-delete">Excluir</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>
`;

export const adicionarGenericoTemplate = () => `
    <div class="page-container">
        <h1>Novo Ativo Genérico</h1>
        <form id="formGenerico" class="form-container">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required>
            </div>
            <div class="form-group">
                <label for="quantidade">Quantidade:</label>
                <input type="number" id="quantidade" name="quantidade" min="0" required>
            </div>
            <div class="form-group">
                <label for="localizacao">Localização:</label>
                <input type="text" id="localizacao" name="localizacao" required>
            </div>
            <div class="form-group">
                <label for="descricao">Descrição:</label>
                <textarea id="descricao" name="descricao" rows="3"></textarea>
            </div>
            <input type="submit" value="Adicionar" class="btn-submit">
            <a href="/genericos" class="btn-link">Voltar</a>
        </form>
    </div>
`;

export const notificacoesTemplate = (notificacoes) => `
    <div class="page-container">
        <h1>Notificações</h1>
        <div class="notifications-list">
            ${notificacoes.map(notif => `
                <div class="notification-item ${notif.lida ? 'read' : 'unread'}">
                    <div class="notification-header">
                        <span class="notification-type">${notif.tipo}</span>
                        <span class="notification-date">${new Date(notif.data).toLocaleDateString()}</span>
                    </div>
                    <div class="notification-content">
                        <p>${notif.mensagem}</p>
                    </div>
                    ${!notif.lida ? `
                        <button onclick="marcarComoLida('${notif.id}')" class="btn-link">
                            Marcar como lida
                        </button>
                    ` : ''}
                </div>
            `).join('')}
        </div>
        ${notificacoes.length === 0 ? `
            <div class="empty-state">
                <p>Nenhuma notificação encontrada</p>
            </div>
        ` : ''}
    </div>
`;