# ConstruBrito — PostgreSQL (Docker) sem ORM

Aplicação Django usada **apenas** como roteador + templates.
Toda a persistência é feita com **SQL puro** via `psycopg` (arquivo `core/db.py`).
O PostgreSQL roda em **Docker** (`docker-compose.yml`) e o schema é aplicado
automaticamente pelo arquivo `schema.sql` na primeira inicialização do container.

## 1. Pré-requisitos
- Docker Desktop (com Docker Compose)
- Python 3.11+

## 2. Subir o banco
```bash
docker compose up -d
# o schema.sql é executado automaticamente na 1ª vez
```

Conexão padrão:
```
host=localhost  port=5432  db=construbrito  user=construbrito  pwd=construbrito
```

## 3. Rodar o Django
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env        # (Linux/Mac: cp .env.example .env)
python manage.py runserver
```

Abra http://localhost:8000

## 4. Resetar o banco
```bash
docker compose down -v   # apaga o volume
docker compose up -d     # recria + roda schema.sql
```

## Estrutura
```
schema.sql              ← DDL PostgreSQL (executado pelo Docker)
docker-compose.yml      ← Serviço Postgres
core/db.py              ← Acesso a dados em SQL puro (psycopg)
core/views.py           ← Views Django chamando core/db.py
core/templates/core/    ← Templates HTML
core/static/css/        ← Estilos
construbrito/settings.py← Sem auth/admin/ORM
```

