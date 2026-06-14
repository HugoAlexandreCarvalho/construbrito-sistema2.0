-- script que cria todas as tabelas do sistema
-- o docker roda esse arquivo sozinho quando sobe o banco pela primeira vez

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- tabela de categorias dos produtos
CREATE TABLE IF NOT EXISTS categorias (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome        VARCHAR(100) NOT NULL UNIQUE,
    descricao   TEXT DEFAULT '',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- tabela dos produtos da loja
CREATE TABLE IF NOT EXISTS produtos (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo          VARCHAR(50) NOT NULL UNIQUE,
    nome            VARCHAR(200) NOT NULL,
    descricao       TEXT DEFAULT '',
    categoria_id    UUID REFERENCES categorias(id) ON DELETE SET NULL,
    unidade         VARCHAR(10) NOT NULL DEFAULT 'un',
    preco_custo     NUMERIC(10,2) NOT NULL DEFAULT 0,
    preco_venda     NUMERIC(10,2) NOT NULL DEFAULT 0,
    estoque_minimo  INTEGER NOT NULL DEFAULT 0,
    estoque_atual   INTEGER NOT NULL DEFAULT 0,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);

-- tabela dos clientes
CREATE TABLE IF NOT EXISTS clientes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome            VARCHAR(200) NOT NULL,
    cpf_cnpj        VARCHAR(20) UNIQUE,
    telefone        VARCHAR(20) DEFAULT '',
    email           VARCHAR(150) DEFAULT '',
    endereco        TEXT DEFAULT '',
    limite_credito  NUMERIC(10,2) NOT NULL DEFAULT 0,
    saldo_devedor   NUMERIC(10,2) NOT NULL DEFAULT 0,
    status_credito  VARCHAR(20) NOT NULL DEFAULT 'novo',
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- cada venda feita na loja
CREATE TABLE IF NOT EXISTS vendas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo          VARCHAR(20) NOT NULL UNIQUE,
    cliente_id      UUID NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    status          VARCHAR(20) NOT NULL DEFAULT 'finalizada',
    tipo_pagamento  VARCHAR(20) NOT NULL DEFAULT 'avista',
    parcelas        INTEGER NOT NULL DEFAULT 1,
    subtotal        NUMERIC(10,2) NOT NULL DEFAULT 0,
    desconto        NUMERIC(10,2) NOT NULL DEFAULT 0,
    total           NUMERIC(10,2) NOT NULL DEFAULT 0,
    observacoes     TEXT DEFAULT '',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- os produtos que entraram em cada venda
CREATE TABLE IF NOT EXISTS itens_venda (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venda_id        UUID NOT NULL REFERENCES vendas(id) ON DELETE CASCADE,
    produto_id      UUID NOT NULL REFERENCES produtos(id) ON DELETE RESTRICT,
    quantidade      NUMERIC(10,3) NOT NULL DEFAULT 1,
    preco_praticado NUMERIC(10,2) NOT NULL DEFAULT 0,
    subtotal        NUMERIC(10,2) NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_itens_venda_venda ON itens_venda(venda_id);

-- parcelas das vendas a prazo
CREATE TABLE IF NOT EXISTS contas_a_receber (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venda_id        UUID NOT NULL REFERENCES vendas(id) ON DELETE CASCADE,
    data_vencimento DATE NOT NULL,
    valor_parcela   NUMERIC(10,2) NOT NULL,
    data_pagamento  DATE,
    status          VARCHAR(20) NOT NULL DEFAULT 'pendente',
    observacoes     TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_contas_venda ON contas_a_receber(venda_id);
CREATE INDEX IF NOT EXISTS idx_contas_status ON contas_a_receber(status);

-- ja deixa algumas categorias prontas pra nao começar do zero
INSERT INTO categorias (nome, descricao) VALUES
    ('Cimento', 'Cimentos e argamassas'),
    ('Ferragens', 'Pregos, parafusos e ferramentas'),
    ('Hidráulica', 'Tubos, conexões e registros'),
    ('Elétrica', 'Fios, disjuntores e tomadas')
ON CONFLICT (nome) DO NOTHING;
