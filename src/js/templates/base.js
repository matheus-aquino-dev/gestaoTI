export const baseTemplate = (content) => `
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestão de Ativos TI</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="nav-logo">GestãoTI</a>
            <div class="nav-menu">
                <a href="/ativos">Ativos</a>
                <a href="/usuarios">Usuários</a>
                <a href="/categorias">Categorias</a>
                <a href="/demandas">Demandas</a>
                <a href="/logout">Sair</a>
            </div>
        </div>
    </nav>
    <main class="container">
        ${content}
    </main>
    <script type="module" src="/static/js/main.js"></script>
</body>
</html>`;