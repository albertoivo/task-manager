## 🚀 Task Manager API – Gerenciador de Tarefas com Prioridade e Agendamentos

---

### 🎯 Objetivo:

Criar uma API RESTful (usando **FastAPI**) que permita aos usuários:

* Criar, listar, atualizar e excluir tarefas.
* Definir níveis de prioridade (ex: low, medium, high).
* Marcar tarefas como concluídas.
* Agendar tarefas com datas futuras.
* Enviar **notificações simuladas** (exemplo: logging ou simular um envio de e-mail) para tarefas agendadas próximas da data de vencimento (via **background jobs**).

---

### ✅ Motivos para escolher esse projeto:

1. **Modelagem de domínio um pouco mais rica que um simples CRUD** (tem estados, prioridades, agendamentos...).
2. Permite aplicar conceitos como:

   * **Background tasks** (FastAPI BackgroundTasks ou Celery + Redis)
   * **Cache (Redis)** para listagens rápidas de tarefas
   * **Filtros / paginação / ordenação nas APIs**
   * **Validação de dados com Pydantic models mais complexos**
3. Você pode reutilizar como **template para sistemas maiores (ex: ToDo apps, schedulers, workflow engines)**.
4. É pequeno o suficiente para terminar rápido (em 1 a 2 semanas, no máximo, estudando em paralelo).

---

### 🛠️ Tecnologias e boas práticas recomendadas:

* **FastAPI** → API layer.
* **Pydantic** → Modelagem de schemas / validações.
* **SQLAlchemy** → ORM + Persistência.
* **SQLite ou PostgreSQL** → Banco de dados.
* **Redis** → Cache (para GET de tarefas) e filas de background jobs (se quiser ir além, usar **Celery**).
* **Alembic** → Migrações de banco de dados.
* **Pytest** → Testes unitários e de integração.
* **Docker** → Containerizar a aplicação (opcional, mas recomendado).
* **Logging estruturado (Python logging)** → Para produção.

---

### 📋 Requisitos detalhados do projeto:

#### Endpoints principais:

| Método | Endpoint                   | Descrição                                                             |
| ------ | -------------------------- | --------------------------------------------------------------------- |
| POST   | /tasks                     | Criar uma nova tarefa                                                 |
| GET    | /tasks                     | Listar todas as tarefas (com filtros: status, prioridade, vencimento) |
| GET    | /tasks/{task\_id}          | Detalhar uma tarefa                                                   |
| PUT    | /tasks/{task\_id}          | Atualizar uma tarefa                                                  |
| DELETE | /tasks/{task\_id}          | Deletar uma tarefa                                                    |
| POST   | /tasks/{task\_id}/complete | Marcar como concluída                                                 |

#### Funcionalidades adicionais:

* **Filtros por status (pending/completed), prioridade e duo date**
* **Cache para GET /tasks**
* **Notificação simulada via background task antes do vencimento (ex: 1 hora antes)**
* **Autenticação com JWT (reuso da estrutura anterior)**

---

### 📈 O que você vai aprender de novo:

* Trabalhar com **BackgroundTasks** ou **Celery**.
* Implementar **cache de leitura** (Redis + FastAPI).
* Melhorar a **modelagem Pydantic (nested models)**.
* Criar filtros dinâmicos e paginação.
* Testar tarefas assíncronas.
* Configurar **docker-compose** com Redis + Banco + App (se quiser dar um passo a mais).
