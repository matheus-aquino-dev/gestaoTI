import { loginTemplate, registerTemplate } from './templates/usuariosTemplates.js';
import { listarAtivosTemplate, adicionarAtivoTemplate } from './templates/ativosTemplates.js';
import { listarCategoriasTemplate, adicionarCategoriaTemplate } from './templates/categoriasTemplates.js';
import { listarDemandasTemplate, novaDemandaTemplate } from './templates/demandasTemplates.js';
import { listarCentroCustoTemplate, adicionarCentroCustoTemplate } from './templates/centroCustoTemplates.js';

class Router {
    constructor(rootElement) {
        this.root = rootElement;
        this.routes = new Map();
        this.init();
    }

    init() {
        window.addEventListener('popstate', () => this.handleRoute());
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href]')) {
                e.preventDefault();
                const href = e.target.getAttribute('href');
                this.navigate(href);
            }
        });
    }

    addRoute(path, handler) {
        this.routes.set(path, handler);
    }

    navigate(path) {
        window.history.pushState({}, '', path);
        this.handleRoute();
    }

    async handleRoute() {
        const path = window.location.pathname;
        const handler = this.routes.get(path) || this.routes.get('*');
        
        if (handler) {
            try {
                const content = await handler();
                this.root.innerHTML = content;
            } catch (error) {
                console.error('Erro ao carregar rota:', error);
                this.root.innerHTML = '<div class="error">Erro ao carregar página</div>';
            }
        }
    }
}

// Instancia o router
const router = new Router(document.getElementById('app'));

// Configura as rotas
router.addRoute('/', () => listarAtivosTemplate([]));
router.addRoute('/login', () => loginTemplate());
router.addRoute('/register', () => registerTemplate());
router.addRoute('/ativos', () => listarAtivosTemplate([]));
router.addRoute('/adicionar-ativo', () => adicionarAtivoTemplate([]));
router.addRoute('/categorias', () => listarCategoriasTemplate([]));
router.addRoute('/adicionar-categoria', () => adicionarCategoriaTemplate());
router.addRoute('/demandas', () => listarDemandasTemplate([]));
router.addRoute('/nova-demanda', () => novaDemandaTemplate());
router.addRoute('/centro-custo', () => listarCentroCustoTemplate([]));
router.addRoute('/adicionar-centro-custo', () => adicionarCentroCustoTemplate());

// Rota padrão para página não encontrada
router.addRoute('*', () => `
    <div class="error-page">
        <h1>404 - Página não encontrada</h1>
        <a href="/" class="btn-link">Voltar para Home</a>
    </div>
`);

export default router;