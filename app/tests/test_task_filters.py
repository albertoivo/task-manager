from datetime import datetime, timedelta
from urllib.parse import quote

import pytest
from fastapi import status


class TestTaskFilters:
    """Testes para filtros e buscas de tarefas."""

    @pytest.fixture(autouse=True)
    def setup_test_data(self, client):
        """Cria dados de teste para serem usados nos filtros."""
        # Criar tarefas com diferentes características
        self.test_tasks = [
            {
                "title": "Tarefa urgente 1",
                "description": "Implementar autenticação",
                "status": "pending",
                "priority": "high",
                "assigned_to": "João Silva",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            },
            {
                "title": "Tarefa em progresso",
                "description": "Desenvolver API REST",
                "status": "in_progress",
                "priority": "medium",
                "assigned_to": "Maria Santos",
                "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
            },
            {
                "title": "Tarefa concluída",
                "description": "Configurar banco de dados",
                "status": "completed",
                "priority": "high",
                "assigned_to": "João Silva",
                "due_date": (datetime.now() - timedelta(days=2)).isoformat(),
            },
            {
                "title": "Tarefa atrasada",
                "description": "Escrever documentação",
                "status": "pending",
                "priority": "low",
                "assigned_to": "Ana Costa",
                "due_date": (datetime.now() - timedelta(days=3)).isoformat(),
            },
            {
                "title": "Tarefa para hoje",
                "description": "Revisar código",
                "status": "in_progress",
                "priority": "medium",
                "assigned_to": "Maria Santos",
                "due_date": datetime.now().isoformat(),
            },
        ]

        # Criar as tarefas no banco de teste
        self.created_task_ids = []
        for task_data in self.test_tasks:
            response = client.post("/tasks/", json=task_data)
            self.created_task_ids.append(response.json()["id"])

    def test_filter_by_status_pending(self, client):
        """Testa filtro por status 'pending'."""
        response = client.get("/tasks/filter/status/pending")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2  # 2 tarefas pending

        for task in tasks:
            assert task["status"] == "pending"

    def test_filter_by_status_in_progress(self, client):
        """Testa filtro por status 'in_progress'."""
        response = client.get("/tasks/filter/status/in_progress")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2  # 2 tarefas in_progress

        for task in tasks:
            assert task["status"] == "in_progress"

    def test_filter_by_status_completed(self, client):
        """Testa filtro por status 'completed'."""
        response = client.get("/tasks/filter/status/completed")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1  # 1 tarefa completed

        for task in tasks:
            assert task["status"] == "completed"

    def test_filter_by_invalid_status(self, client):
        """Testa filtro com status inválido."""
        response = client.get("/tasks/filter/status/invalid_status")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_filter_by_priority_high(self, client):
        """Testa filtro por prioridade 'high'."""
        response = client.get("/tasks/filter/priority/high")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2  # 2 tarefas high priority

        for task in tasks:
            assert task["priority"] == "high"

    def test_filter_by_priority_medium(self, client):
        """Testa filtro por prioridade 'medium'."""
        response = client.get("/tasks/filter/priority/medium")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2  # 2 tarefas medium priority

        for task in tasks:
            assert task["priority"] == "medium"

    def test_filter_by_priority_low(self, client):
        """Testa filtro por prioridade 'low'."""
        response = client.get("/tasks/filter/priority/low")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1  # 1 tarefa low priority

        for task in tasks:
            assert task["priority"] == "low"

    def test_filter_by_assigned_to(self, client):
        """Testa filtro por pessoa responsável."""
        response = client.get("/tasks/filter/assigned/João Silva")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2  # 2 tarefas do João Silva

        for task in tasks:
            assert task["assigned_to"] == "João Silva"

    def test_filter_by_assigned_to_with_spaces(self, client):
        """Testa filtro por pessoa com nome que tem espaços."""
        response = client.get("/tasks/filter/assigned/Maria Santos")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2  # 2 tarefas da Maria Santos

        for task in tasks:
            assert task["assigned_to"] == "Maria Santos"

    def test_filter_by_nonexistent_assigned_to(self, client):
        """Testa filtro por pessoa que não existe."""
        response = client.get("/tasks/filter/assigned/Pessoa Inexistente")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 0

    def test_get_overdue_tasks(self, client):
        """Testa busca de tarefas atrasadas."""
        response = client.get("/tasks/overdue")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1  # 1 tarefa atrasada (pending + data passada)

        overdue_task = tasks[0]
        assert overdue_task["title"] == "Tarefa atrasada"
        assert overdue_task["status"] != "completed"

    def test_get_tasks_due_soon_default(self, client):
        """Testa busca de tarefas que vencem em breve (padrão 7 dias)."""
        response = client.get("/tasks/due-soon")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        # Deve retornar tarefas que vencem em 1 dia, 5 dias e hoje
        # mas não a atrasada nem a concluída
        assert len(tasks) >= 2

    def test_get_tasks_due_soon_custom_days(self, client):
        """Testa busca de tarefas que vencem em breve com período customizado."""
        response = client.get("/tasks/due-soon?days=2")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        # Deve retornar tarefas que vencem em 1 dia e hoje
        assert len(tasks) >= 1

    def test_get_tasks_due_today(self, client):
        """Testa busca de tarefas que vencem hoje."""
        response = client.get("/tasks/due-today")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1  # 1 tarefa para hoje

        today_task = tasks[0]
        assert today_task["title"] == "Tarefa para hoje"

    def test_search_tasks_by_title(self, client):
        """Testa busca por texto no título."""
        response = client.get("/tasks/search?q=urgente")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1
        assert "urgente" in tasks[0]["title"].lower()

    def test_search_tasks_by_description(self, client):
        """Testa busca por texto na descrição."""
        response = client.get("/tasks/search?q=API")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1
        assert "API" in tasks[0]["description"]

    def test_search_tasks_case_insensitive(self, client):
        """Testa busca case-insensitive."""
        response = client.get("/tasks/search?q=IMPLEMENTAR")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1
        assert "implementar" in tasks[0]["description"].lower()

    def test_search_tasks_no_results(self, client):
        """Testa busca que não retorna resultados."""
        response = client.get("/tasks/search?q=inexistente")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 0

    def test_search_tasks_missing_query(self, client):
        """Testa busca sem fornecer termo de busca."""
        response = client.get("/tasks/search")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_advanced_filter_single_criterion(self, client):
        """Testa filtro avançado com um único critério."""
        response = client.get("/tasks/filter?status=pending")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2

        for task in tasks:
            assert task["status"] == "pending"

    def test_advanced_filter_multiple_criteria(self, client):
        """Testa filtro avançado com múltiplos critérios."""
        response = client.get("/tasks/filter?status=pending&priority=high")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1

        task = tasks[0]
        assert task["status"] == "pending"
        assert task["priority"] == "high"

    def test_advanced_filter_with_search(self, client):
        """Testa filtro avançado combinado com busca textual."""
        response = client.get("/tasks/filter?status=in_progress&search=API")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 1

        task = tasks[0]
        assert task["status"] == "in_progress"
        assert "API" in task["description"]

    def test_advanced_filter_with_assigned_to(self, client):
        """Testa filtro avançado por pessoa responsável."""
        response = client.get("/tasks/filter?assigned_to=João Silva&priority=high")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 2

        for task in tasks:
            assert task["assigned_to"] == "João Silva"
            assert task["priority"] == "high"

    def test_advanced_filter_no_results(self, client):
        """Testa filtro avançado que não retorna resultados."""
        response = client.get("/tasks/filter?status=completed&priority=low")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 0

    def test_advanced_filter_no_criteria(self, client):
        """Testa filtro avançado sem critérios (deve retornar todas)."""
        response = client.get("/tasks/filter")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 5  # todas as tarefas de teste

    def test_filters_with_date_range(self, client):
        """Testa filtro por intervalo de datas."""
        start_datetime = datetime.now() - timedelta(days=1)
        end_datetime = datetime.now() + timedelta(days=3)

        # Formato ISO com URL encoding
        start_date = quote(start_datetime.isoformat())
        end_date = quote(end_datetime.isoformat())

        response = client.get(
            f"/tasks/filter?start_date={start_date}&end_date={end_date}"
        )
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) >= 2
