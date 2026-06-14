# Sistema Construbrito
## Equipe Responsável

### Hugo Alexandre Carvalho Coelho Coutinho

Responsável pelo levantamento de requisitos do sistema, identificação das necessidades da empresa e apoio na modelagem das funcionalidades.

### Jeferson Machado dos Santos

Responsável pela modelagem e implementação do banco de dados PostgreSQL, integração entre aplicação e banco de dados e desenvolvimento da camada de persistência.

### Gustavo Barros Martins

Responsável pelo desenvolvimento das funcionalidades do sistema, implementação da interface web e realização de testes.

---

# Introdução

O Sistema Construbrito foi desenvolvido com o objetivo de modernizar e automatizar os processos internos de uma loja de materiais de construção.

Durante o levantamento de requisitos realizado junto à empresa, foram identificadas dificuldades relacionadas ao controle de estoque, gerenciamento de clientes, acompanhamento de vendas e controle financeiro das contas a receber.

A partir dessas necessidades foi proposta uma solução web que centraliza as operações da empresa em um único sistema, proporcionando maior organização, agilidade e confiabilidade das informações.

Nesta nova versão do projeto, o sistema evoluiu de uma aplicação simples em terminal para uma aplicação web desenvolvida com Django, utilizando PostgreSQL como banco de dados e Docker para gerenciamento da infraestrutura.

---

# Problema Identificado

A empresa enfrentava dificuldades em atividades fundamentais para sua operação, como:

* Controle manual de estoque;
* Cadastro e consulta de clientes;
* Registro de vendas;
* Controle de crédito dos clientes;
* Acompanhamento de parcelas pendentes;
* Organização das informações financeiras;
* Controle de produtos por categoria.

Esses processos geravam retrabalho, possibilidade de erros e dificuldades na tomada de decisão.

---

# Solução Proposta

O Sistema Construbrito foi desenvolvido para centralizar e automatizar os principais processos da empresa, oferecendo uma solução capaz de:

* Gerenciar produtos e categorias;
* Controlar estoque automaticamente;
* Realizar cadastro de clientes;
* Registrar vendas à vista e parceladas;
* Gerenciar contas a receber;
* Acompanhar o limite de crédito dos clientes;
* Disponibilizar informações gerenciais através de um painel de controle.

---

# Objetivos do Sistema

## Objetivo Geral

Automatizar os processos administrativos e comerciais da empresa, aumentando a eficiência operacional e reduzindo erros manuais.

## Objetivos Específicos

* Cadastrar e gerenciar clientes;
* Controlar o estoque de produtos;
* Organizar produtos por categorias;
* Registrar vendas;
* Gerenciar pagamentos parcelados;
* Controlar o crédito disponível dos clientes;
* Disponibilizar informações gerenciais através de dashboards;
* Garantir integridade dos dados armazenados.

---

# Tecnologias Utilizadas

* Python 3.11+
* Django
* PostgreSQL
* Psycopg
* Docker
* Docker Compose
* HTML5
* CSS3
* GitHub
* Visual Studio Code

---

# Estrutura do Projeto

```text
construbrito-sistema2.0/

├── construbrito/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── db.py
│   ├── views.py
│   ├── urls.py
│   │
│   ├── templates/
│   │   └── core/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── categorias.html
│   │       ├── produtos.html
│   │       ├── clientes.html
│   │       ├── vendas.html
│   │       └── contas.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── schema.sql
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── .env
└── .env.example
```

---

# Funcionalidades Implementadas

## 1. Dashboard

Apresenta informações gerais do sistema, facilitando o acompanhamento das operações da empresa.

---

## 2. Gerenciamento de Categorias

Permite:

* Cadastro de categorias;
* Consulta de categorias;
* Exclusão de categorias.

---

## 3. Gerenciamento de Produtos

Permite:

* Cadastro de produtos;
* Associação de produtos a categorias;
* Controle de estoque;
* Definição de estoque mínimo;
* Controle de preços de custo e venda;
* Consulta de produtos.

---

## 4. Gerenciamento de Clientes

Permite:

* Cadastro de clientes;
* Armazenamento de dados de contato;
* Controle de limite de crédito;
* Consulta de clientes;
* Exclusão de clientes.

---

## 5. Registro de Vendas

Permite:

* Registro de vendas com múltiplos itens;
* Aplicação de descontos;
* Controle de formas de pagamento;
* Vendas à vista;
* Vendas parceladas;
* Geração automática dos itens da venda.

---

## 6. Controle Automático de Estoque

Após cada venda, o sistema realiza automaticamente a atualização do estoque dos produtos comercializados.

---

## 7. Contas a Receber

Permite:

* Controle das parcelas geradas nas vendas;
* Acompanhamento de pagamentos pendentes;
* Registro de pagamentos realizados;
* Consulta de contas abertas.

---

## 8. Controle de Crédito

O sistema mantém o saldo devedor dos clientes e permite acompanhar o crédito disponível para novas compras.

---

# Arquitetura do Sistema

O projeto utiliza uma arquitetura baseada em separação de responsabilidades:

### Camada de Apresentação

Responsável pelas páginas HTML e interação com o usuário.

* Templates Django
* HTML
* CSS

### Camada de Aplicação

Responsável pelas regras de negócio.

* Views Django

### Camada de Persistência

Responsável pela comunicação com o banco de dados.

* SQL Puro
* Psycopg
* PostgreSQL

---

# Persistência de Dados

Diferentemente da abordagem tradicional do Django, este projeto não utiliza ORM.

Toda a comunicação com o banco de dados é realizada através de comandos SQL escritos manualmente no arquivo:

```text
core/db.py
```

Essa abordagem proporciona maior controle sobre consultas, transações e desempenho da aplicação.

---

# Estado Atual do Sistema

O sistema encontra-se em uma versão funcional avançada, contendo:

* Interface web completa;
* Banco de dados PostgreSQL;
* Integração via Docker;
* Controle de estoque;
* Cadastro de clientes;
* Cadastro de produtos;
* Cadastro de categorias;
* Registro de vendas;
* Controle de crédito;
* Contas a receber;
* Dashboard administrativo.

---

# Roteiro de Evolução Futura

* Relatórios gerenciais;
* Controle de fornecedores;
* Controle de compras;
* Emissão de notas fiscais;
* Controle de usuários e permissões;
* Exportação de relatórios em PDF;
* Gráficos e indicadores avançados.

---

# Link do Repositório

https://github.com/HugoAlexandreCarvalho/construbrito-sistema2.0

---

# Instruções para Execução do Sistema

## 1. Pré-requisitos

* Docker Desktop (com Docker Compose)
* Python 3.11+

## 2. Subir o banco

```bash
docker compose up -d
```

O arquivo `schema.sql` será executado automaticamente na primeira inicialização.

### Conexão padrão

```text
host=localhost
port=5432
database=construbrito
user=construbrito
password=construbrito
```

---

## 3. Executar a aplicação

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Copiar arquivo de configuração:

```bash
copy .env.example .env
```

Linux/Mac:

```bash
cp .env.example .env
```

Executar servidor:

```bash
python manage.py runserver
```

Abrir:

```text
http://localhost:8000
```

---

## 4. Resetar o Banco

```bash
docker compose down -v
docker compose up -d
```

O volume será recriado e o `schema.sql` será executado novamente.
