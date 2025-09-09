export const loginTemplate = () => `
    <div class="auth-container">
        <div class="auth-card">
            <h1>Login</h1>
            <form id="loginForm" class="auth-form">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="senha">Senha</label>
                    <input type="password" id="senha" name="senha" required>
                </div>
                <button type="submit" class="btn-primary btn-block">Entrar</button>
                <p class="auth-links">
                    Não tem uma conta? <a href="/register" class="nav-link">Registre-se</a>
                </p>
            </form>
        </div>
    </div>
`;

export const registerTemplate = () => `
    <div class="auth-container">
        <div class="auth-card">
            <h1>Registro</h1>
            <form id="registerForm" class="auth-form">
                <div class="form-group">
                    <label for="nome">Nome completo</label>
                    <input type="text" id="nome" name="nome" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
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
                    <label for="senha">Senha</label>
                    <input type="password" id="senha" name="senha" required>
                </div>
                <div class="form-group">
                    <label for="confirmarSenha">Confirmar Senha</label>
                    <input type="password" id="confirmarSenha" name="confirmarSenha" required>
                </div>
                <button type="submit" class="btn-primary btn-block">Registrar</button>
                <p class="auth-links">
                    Já tem uma conta? <a href="/login" class="nav-link">Faça login</a>
                </p>
            </form>
        </div>
    </div>
`;