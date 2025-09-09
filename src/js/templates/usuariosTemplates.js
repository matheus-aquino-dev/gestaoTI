import { baseTemplate } from './base.js';

export const loginTemplate = () => `
    <div class="login-container">
        <h1>Login</h1>
        <form id="formLogin" class="form-container">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" name="email" id="email" required>
            </div>
            <div class="form-group">
                <label for="senha">Senha:</label>
                <input type="password" name="senha" id="senha" required>
            </div>
            <input type="submit" value="Entrar" class="btn-submit">
            <a href="/register" class="btn-link">Registrar</a>
        </form>
    </div>
`;

export const registerTemplate = () => `
    <div class="register-container">
        <h1>Registro</h1>
        <form id="formRegister" class="form-container">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" name="nome" id="nome" required>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" name="email" id="email" required>
            </div>
            <div class="form-group">
                <label for="senha">Senha:</label>
                <input type="password" name="senha" id="senha" required>
            </div>
            <div class="form-group">
                <label for="confirmarSenha">Confirmar Senha:</label>
                <input type="password" name="confirmarSenha" id="confirmarSenha" required>
            </div>
            <input type="submit" value="Registrar" class="btn-submit">
            <a href="/login" class="btn-link">Já tem conta? Faça login</a>
        </form>
    </div>
`;

export const listarUsuariosTemplate = (usuarios) => `
    <div class="page-container">
        <h1>Usuários</h1>
        <div class="actions-container">
            <button onclick="window.location.href='/adicionar-usuario'" class="btn-primary">Novo Usuário</button>
        </div>
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Perfil</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${usuarios.map(usuario => `
                        <tr>
                            <td>${usuario.nome}</td>
                            <td>${usuario.email}</td>
                            <td>${usuario.perfil}</td>
                            <td class="actions">
                                <button onclick="editarUsuario('${usuario.id}')" class="btn-edit">Editar</button>
                                <button onclick="excluirUsuario('${usuario.id}')" class="btn-delete">Excluir</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>
`;