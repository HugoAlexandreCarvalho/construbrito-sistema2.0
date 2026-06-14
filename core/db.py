# aqui ficam todas as funcoes que falam com o banco
# nao usamos ORM, é tudo SQL na mao com o psycopg
from contextlib import contextmanager
from typing import Any, Iterable, Optional
import psycopg
from psycopg.rows import dict_row
from django.conf import settings


# funcao que abre a conexao com o postgres

def _connect() -> psycopg.Connection:
    return psycopg.connect(**settings.POSTGRES_CONFIG, row_factory=dict_row)


@contextmanager
def cursor():
    # abre um cursor e ja faz commit no final (ou rollback se der erro)
    conn = _connect()
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def transaction():
    # usado quando precisa rodar varias coisas dentro de uma transacao so
    conn = _connect()
    try:
        with conn.transaction():
            yield conn
    finally:
        conn.close()


# atalhos pra nao precisar repetir codigo

def fetchall(sql: str, params: Iterable[Any] = ()) -> list[dict]:
    with cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def fetchone(sql: str, params: Iterable[Any] = ()) -> Optional[dict]:
    with cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def execute(sql: str, params: Iterable[Any] = ()) -> None:
    with cursor() as cur:
        cur.execute(sql, params)


# ===== daqui pra baixo vao as funcoes de cada parte do sistema =====

# ----- categorias -----
def list_categorias() -> list[dict]:
    return fetchall("SELECT * FROM categorias ORDER BY nome")

def create_categoria(nome: str, descricao: str = '') -> None:
    execute(
        "INSERT INTO categorias (nome, descricao) VALUES (%s, %s)",
        (nome, descricao),
    )

def delete_categoria(cid) -> None:
    execute("DELETE FROM categorias WHERE id = %s", (cid,))


# ----- produtos -----
def list_produtos() -> list[dict]:
    return fetchall("""
        SELECT p.*, c.nome AS categoria_nome
        FROM produtos p
        LEFT JOIN categorias c ON c.id = p.categoria_id
        ORDER BY p.nome
    """)

def create_produto(data: dict) -> None:
    execute("""
        INSERT INTO produtos
            (codigo, nome, descricao, categoria_id, unidade,
             preco_custo, preco_venda, estoque_minimo, estoque_atual, ativo)
        VALUES (%(codigo)s, %(nome)s, %(descricao)s, %(categoria_id)s, %(unidade)s,
                %(preco_custo)s, %(preco_venda)s, %(estoque_minimo)s, %(estoque_atual)s, %(ativo)s)
    """, data)

def delete_produto(pid) -> None:
    execute("DELETE FROM produtos WHERE id = %s", (pid,))


# ----- clientes -----
def list_clientes() -> list[dict]:
    return fetchall("""
        SELECT *, (limite_credito - saldo_devedor) AS credito_disponivel
        FROM clientes ORDER BY nome
    """)

def create_cliente(data: dict) -> None:
    execute("""
        INSERT INTO clientes
            (nome, cpf_cnpj, telefone, email, endereco,
             limite_credito, status_credito)
        VALUES (%(nome)s, %(cpf_cnpj)s, %(telefone)s, %(email)s, %(endereco)s,
                %(limite_credito)s, %(status_credito)s)
    """, data)

def delete_cliente(cid) -> None:
    execute("DELETE FROM clientes WHERE id = %s", (cid,))


# ----- vendas -----
def list_vendas() -> list[dict]:
    return fetchall("""
        SELECT v.*, c.nome AS cliente_nome
        FROM vendas v
        JOIN clientes c ON c.id = v.cliente_id
        ORDER BY v.created_at DESC
        LIMIT 200
    """)


def create_venda(cliente_id, itens: list[dict], desconto: float,
                 tipo_pagamento: str, parcelas: int, observacoes: str = '') -> str:
    # cria a venda, salva os itens, baixa o estoque
    # se a venda for a prazo, gera as parcelas e ja soma no que o cliente deve
    # tudo dentro de uma transacao pra nao deixar o banco bagunçado
    from datetime import date
    from uuid import uuid4

    def add_months(d: date, n: int) -> date:
        m = d.month - 1 + n
        y = d.year + m // 12
        m = m % 12 + 1
        from calendar import monthrange
        return date(y, m, min(d.day, monthrange(y, m)[1]))

    codigo = uuid4().hex[:8].upper()
    subtotal = sum(float(i['quantidade']) * float(i['preco_praticado']) for i in itens)
    total = max(0.0, subtotal - float(desconto or 0))

    with transaction() as conn:
        with conn.cursor() as cur:
            # primeiro grava a venda na tabela
            cur.execute("""
                INSERT INTO vendas
                    (codigo, cliente_id, tipo_pagamento, parcelas,
                     subtotal, desconto, total, observacoes, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'finalizada')
                RETURNING id
            """, (codigo, cliente_id, tipo_pagamento, parcelas,
                  subtotal, desconto, total, observacoes))
            venda_id = cur.fetchone()['id']

            # agora salva cada item e diminui o estoque do produto (o FOR UPDATE trava a linha pra ninguem alterar junto)
            for it in itens:
                sub = float(it['quantidade']) * float(it['preco_praticado'])
                cur.execute(
                    "SELECT estoque_atual FROM produtos WHERE id = %s FOR UPDATE",
                    (it['produto_id'],),
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError("Produto inexistente")
                novo = float(row['estoque_atual']) - float(it['quantidade'])
                if novo < 0:
                    raise ValueError("Estoque insuficiente")
                cur.execute(
                    "UPDATE produtos SET estoque_atual = %s, updated_at = NOW() WHERE id = %s",
                    (novo, it['produto_id']),
                )
                cur.execute("""
                    INSERT INTO itens_venda
                        (venda_id, produto_id, quantidade, preco_praticado, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (venda_id, it['produto_id'], it['quantidade'],
                      it['preco_praticado'], sub))

            # se for a prazo, cria as parcelas e ja aumenta o que o cliente esta devendo
            if tipo_pagamento == 'aprazo' and parcelas > 0:
                valor = round(total / parcelas, 2)
                hoje = date.today()
                for i in range(parcelas):
                    venc = add_months(hoje, i + 1)
                    cur.execute("""
                        INSERT INTO contas_a_receber
                            (venda_id, data_vencimento, valor_parcela)
                        VALUES (%s, %s, %s)
                    """, (venda_id, venc, valor))

                cur.execute(
                    "UPDATE clientes SET saldo_devedor = saldo_devedor + %s WHERE id = %s",
                    (total, cliente_id),
                )
    return codigo


# ----- contas a receber -----
def list_contas() -> list[dict]:
    return fetchall("""
        SELECT cr.*, v.codigo AS venda_codigo, c.nome AS cliente_nome
        FROM contas_a_receber cr
        JOIN vendas v ON v.id = cr.venda_id
        JOIN clientes c ON c.id = v.cliente_id
        ORDER BY cr.data_vencimento
    """)

def pagar_conta(conta_id) -> None:
    with transaction() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT valor_parcela, status, venda_id FROM contas_a_receber WHERE id = %s FOR UPDATE",
                (conta_id,),
            )
            conta = cur.fetchone()
            if not conta or conta['status'] == 'pago':
                return
            cur.execute("""
                UPDATE contas_a_receber
                SET status = 'pago', data_pagamento = CURRENT_DATE
                WHERE id = %s
            """, (conta_id,))
            cur.execute(
                "SELECT cliente_id FROM vendas WHERE id = %s",
                (conta['venda_id'],),
            )
            cli = cur.fetchone()
            cur.execute("""
                UPDATE clientes
                SET saldo_devedor = GREATEST(0, saldo_devedor - %s)
                WHERE id = %s
            """, (conta['valor_parcela'], cli['cliente_id']))


# ----- dashboard (numeros gerais) -----
def dashboard_stats() -> dict:
    return fetchone("""
        SELECT
          (SELECT COUNT(*) FROM produtos WHERE ativo) AS total_produtos,
          (SELECT COUNT(*) FROM clientes WHERE ativo) AS total_clientes,
          (SELECT COUNT(*) FROM vendas)              AS total_vendas,
          (SELECT COALESCE(SUM(total),0) FROM vendas WHERE status='finalizada') AS total_faturado,
          (SELECT COALESCE(SUM(valor_parcela),0) FROM contas_a_receber WHERE status='pendente') AS a_receber,
          (SELECT COUNT(*) FROM produtos WHERE estoque_atual <= estoque_minimo AND ativo) AS estoque_baixo
    """) or {}
