export const mockData = {
    ativos: [
        { id: '1', nome: 'Notebook Dell', categoria: 'Notebooks', status: 'em_uso', responsavel: 'João Silva' },
        { id: '2', nome: 'iPhone 12', categoria: 'Smartphones', status: 'disponivel', responsavel: null },
        { id: '3', nome: 'Monitor LG 24"', categoria: 'Monitores', status: 'manutencao', responsavel: null }
    ],
    usuarios: [
        { id: '1', nome: 'João Silva', email: 'joao@exemplo.com', perfil: 'usuario' },
        { id: '2', nome: 'Maria Santos', email: 'maria@exemplo.com', perfil: 'admin' }
    ],
    categorias: [
        { id: '1', nome: 'Notebooks' },
        { id: '2', nome: 'Smartphones' },
        { id: '3', nome: 'Monitores' }
    ]
};