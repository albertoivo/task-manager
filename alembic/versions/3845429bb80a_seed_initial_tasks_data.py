"""seed initial tasks data

Revision ID: 3845429bb80a
Revises: 95f6134fd4cb
Create Date: 2025-06-25 15:01:18.080707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '{seu_novo_id_de_revisao}' # Substitua pelo ID gerado
down_revision: Union[str, None] = '95f6134fd4cb' # ID da migração anterior (criação da tabela)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crie uma definição ad-hoc da tabela 'tasks' para inserir os dados
    tasks_table = table(
        'tasks',
        column('title', sa.String),
        column('description', sa.String),
        column('status', sa.String),
        column('priority', sa.String),
        column('due_date', sa.DateTime),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime),
    )

    # Use op.bulk_insert para inserir múltiplos registros de uma vez
    op.bulk_insert(
        tasks_table,
        [
            {
                'title': 'Configurar ambiente de desenvolvimento',
                'description': 'Instalar Docker, Python e configurar o VS Code.',
                'status': 'completed',
                'priority': 'high',
                'due_date': datetime(2025, 6, 20),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            },
            {
                'title': 'Implementar CRUD de Tarefas',
                'description': 'Criar os endpoints para Create, Read, Update e Delete de tarefas.',
                'status': 'in_progress',
                'priority': 'high',
                'due_date': datetime(2025, 6, 30),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            },
            {
                'title': 'Adicionar testes unitários',
                'description': 'Escrever testes para os serviços e endpoints da API.',
                'status': 'pending',
                'priority': 'medium',
                'due_date': datetime(2025, 7, 5),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            },
            {
                'title': 'Documentar a API com Swagger/OpenAPI',
                'description': 'Revisar os schemas e descrições para que a documentação automática fique clara.',
                'status': 'pending',
                'priority': 'low',
                'due_date': None,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            },
        ]
    )


def downgrade() -> None:
    # A função downgrade deve remover os dados inseridos.
    # Uma forma simples é deletar todos os registros da tabela.
    op.execute("DELETE FROM tasks")