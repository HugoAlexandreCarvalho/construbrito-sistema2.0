from django.urls import path
from core import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('categorias/', views.categorias_list, name='categorias'),
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/<uuid:cid>/excluir/', views.categoria_delete, name='categoria_delete'),

    path('produtos/', views.produtos_list, name='produtos'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<uuid:pid>/excluir/', views.produto_delete, name='produto_delete'),

    path('clientes/', views.clientes_list, name='clientes'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<uuid:cid>/excluir/', views.cliente_delete, name='cliente_delete'),

    path('vendas/', views.vendas_list, name='vendas'),
    path('vendas/nova/', views.venda_create, name='venda_create'),

    path('contas/', views.contas_list, name='contas'),
    path('contas/<uuid:cid>/pagar/', views.conta_pagar, name='conta_pagar'),
]
