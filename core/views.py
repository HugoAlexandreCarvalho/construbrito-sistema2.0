from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from . import db


# pagina inicial com os numeros gerais
def dashboard(request):
    return render(request, 'core/dashboard.html', {
        'stats': db.dashboard_stats(),
        'vendas': db.list_vendas()[:5],
    })


# ===== Categorias =====

def categorias_list(request):
    return render(request, 'core/categorias.html', {'items': db.list_categorias()})

@require_http_methods(['POST'])
def categoria_create(request):
    db.create_categoria(request.POST['nome'], request.POST.get('descricao', ''))
    return redirect('categorias')

@require_http_methods(['POST'])
def categoria_delete(request, cid):
    db.delete_categoria(cid)
    return redirect('categorias')


# ===== Produtos =====

def produtos_list(request):
    return render(request, 'core/produtos.html', {
        'items': db.list_produtos(),
        'categorias': db.list_categorias(),
    })

@require_http_methods(['POST'])
def produto_create(request):
    p = request.POST
    # monta o dicionario pra mandar pro db
    db.create_produto({
        'codigo': p['codigo'],
        'nome': p['nome'],
        'descricao': p.get('descricao', ''),
        'categoria_id': p.get('categoria_id') or None,
        'unidade': p.get('unidade', 'un'),
        'preco_custo': p.get('preco_custo') or 0,
        'preco_venda': p.get('preco_venda') or 0,
        'estoque_minimo': p.get('estoque_minimo') or 0,
        'estoque_atual': p.get('estoque_atual') or 0,
        'ativo': True,
    })
    return redirect('produtos')

@require_http_methods(['POST'])
def produto_delete(request, pid):
    db.delete_produto(pid)
    return redirect('produtos')


# ===== Clientes =====

def clientes_list(request):
    return render(request, 'core/clientes.html', {'items': db.list_clientes()})

@require_http_methods(['POST'])
def cliente_create(request):
    p = request.POST
    db.create_cliente({
        'nome': p['nome'],
        'cpf_cnpj': p.get('cpf_cnpj') or None,
        'telefone': p.get('telefone', ''),
        'email': p.get('email', ''),
        'endereco': p.get('endereco', ''),
        'limite_credito': p.get('limite_credito') or 0,
        'status_credito': p.get('status_credito', 'novo'),
    })
    return redirect('clientes')

@require_http_methods(['POST'])
def cliente_delete(request, cid):
    db.delete_cliente(cid)
    return redirect('clientes')


# ===== Vendas =====

def vendas_list(request):
    return render(request, 'core/vendas.html', {
        'items': db.list_vendas(),
        'clientes': db.list_clientes(),
        'produtos': db.list_produtos(),
    })

@require_http_methods(['POST'])
def venda_create(request):
    p = request.POST
    # os campos do formulario vem como listas (um por item)
    produto_ids = p.getlist('produto_id[]')
    quantidades = p.getlist('quantidade[]')
    precos = p.getlist('preco_praticado[]')
    itens = [
        {'produto_id': pid, 'quantidade': q, 'preco_praticado': pr}
        for pid, q, pr in zip(produto_ids, quantidades, precos) if pid and q
    ]
    try:
        db.create_venda(
            cliente_id=p['cliente_id'],
            itens=itens,
            desconto=p.get('desconto') or 0,
            tipo_pagamento=p.get('tipo_pagamento', 'avista'),
            parcelas=int(p.get('parcelas') or 1),
            observacoes=p.get('observacoes', ''),
        )
    except Exception as e:
        # se der ruim mostra a mensagem na mesma tela
        return render(request, 'core/vendas.html', {
            'items': db.list_vendas(),
            'clientes': db.list_clientes(),
            'produtos': db.list_produtos(),
            'erro': str(e),
        })
    return redirect('vendas')


# ===== Contas a receber =====

def contas_list(request):
    return render(request, 'core/contas.html', {'items': db.list_contas()})

@require_http_methods(['POST'])
def conta_pagar(request, cid):
    db.pagar_conta(cid)
    return redirect('contas')
