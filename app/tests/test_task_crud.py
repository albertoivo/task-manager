from datetime import datetime, timedelta

from fastapi import status


class TestTaskCRUD:
    """Testes para operações CRUD básicas de tarefas."""

    def test_list_tasks_empty(self, client):
        """Testa listagem quando não há tarefas."""
        response = client.get("/tasks/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_task_success(self, client):
        """Testa criação de tarefa com dados válidos."""
        task_data = {
            "title": "Teste de criação",
            "description": "Descrição do teste",
            "status": "pending",
            "priority": "high",
            "due_date": "2025-07-01T10:00:00",
            "assigned_to": "João Silva",
        }

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED

        created_task = response.json()
        assert created_task["title"] == task_data["title"]
        assert created_task["description"] == task_data["description"]
        assert created_task["status"] == task_data["status"]
        assert created_task["priority"] == task_data["priority"]
        assert created_task["assigned_to"] == task_data["assigned_to"]
        assert "id" in created_task
        assert "created_at" in created_task
        assert "updated_at" in created_task

    def test_create_task_minimal_data(self, client):
        """Testa criação de tarefa com dados mínimos obrigatórios."""
        task_data = {"title": "Tarefa mínima"}

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED

        created_task = response.json()
        assert created_task["title"] == task_data["title"]
        assert created_task["status"] == "pending"  # valor padrão
        assert created_task["priority"] == "medium"  # valor padrão

    def test_create_task_invalid_status(self, client):
        """Testa criação de tarefa com status inválido."""
        task_data = {"title": "Teste status inválido", "status": "invalid_status"}

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_task_invalid_priority(self, client):
        """Testa criação de tarefa com prioridade inválida."""
        task_data = {
            "title": "Teste prioridade inválida",
            "priority": "invalid_priority",
        }

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_task_empty_title(self, client):
        """Testa criação de tarefa com título vazio."""
        task_data = {"title": ""}

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_task_success(self, client):
        """Testa busca de tarefa por ID existente."""
        # Primeiro, cria uma tarefa
        task_data = {
            "title": "Tarefa para buscar",
            "description": "Descrição da tarefa",
        }
        create_response = client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]

        # Busca a tarefa criada
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == status.HTTP_200_OK

        found_task = response.json()
        assert found_task["id"] == task_id
        assert found_task["title"] == task_data["title"]
        assert found_task["description"] == task_data["description"]

    def test_get_task_not_found(self, client):
        """Testa busca de tarefa com ID inexistente."""
        response = client.get("/tasks/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    def test_update_task_success(self, client):
        """Testa atualização de tarefa com dados válidos."""
        # Cria uma tarefa
        task_data = {
            "title": "Tarefa original",
            "description": "Descrição original",
            "status": "pending",
        }
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Atualiza a tarefa
        update_data = {
            "title": "Tarefa atualizada",
            "status": "in_progress",
            "priority": "high",
        }

        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK

        updated_task = response.json()
        assert updated_task["title"] == update_data["title"]
        assert updated_task["status"] == update_data["status"]
        assert updated_task["priority"] == update_data["priority"]
        assert updated_task["description"] == task_data["description"]  # não alterado

    def test_update_task_partial(self, client):
        """Testa atualização parcial de tarefa."""
        # Cria uma tarefa
        task_data = {
            "title": "Tarefa original",
            "description": "Descrição original",
            "status": "pending",
            "priority": "low",
        }
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Atualiza apenas o status
        update_data = {"status": "completed"}

        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK

        updated_task = response.json()
        assert updated_task["status"] == "completed"
        assert updated_task["title"] == task_data["title"]  # não alterado
        assert updated_task["priority"] == task_data["priority"]  # não alterado

    def test_update_task_not_found(self, client):
        """Testa atualização de tarefa inexistente."""
        update_data = {"title": "Tarefa que não existe"}

        response = client.put("/tasks/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task_invalid_data(self, client):
        """Testa atualização com dados inválidos."""
        # Cria uma tarefa
        task_data = {"title": "Tarefa para teste"}
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Tenta atualizar com status inválido
        update_data = {"status": "invalid_status"}

        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_task_success(self, client):
        """Testa exclusão de tarefa existente."""
        # Cria uma tarefa
        task_data = {"title": "Tarefa para deletar"}
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Deleta a tarefa
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica que a tarefa foi deletada
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_not_found(self, client):
        """Testa exclusão de tarefa inexistente."""
        response = client.delete("/tasks/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_tasks_after_crud_operations(self, client):
        """Testa listagem após várias operações CRUD."""
        # Cria várias tarefas
        tasks_data = [
            {"title": "Tarefa 1", "priority": "high"},
            {"title": "Tarefa 2", "priority": "medium"},
            {"title": "Tarefa 3", "priority": "low"},
        ]

        created_ids = []
        for task_data in tasks_data:
            response = client.post("/tasks/", json=task_data)
            created_ids.append(response.json()["id"])

        # Lista todas as tarefas
        response = client.get("/tasks/")
        assert response.status_code == status.HTTP_200_OK

        tasks = response.json()
        assert len(tasks) == 3

        # Verifica se todas as tarefas estão na lista
        task_titles = [task["title"] for task in tasks]
        for task_data in tasks_data:
            assert task_data["title"] in task_titles

        # Deleta uma tarefa
        client.delete(f"/tasks/{created_ids[0]}")

        # Verifica que a lista agora tem 2 tarefas
        response = client.get("/tasks/")
        tasks = response.json()
        assert len(tasks) == 2

    def test_create_task_with_future_due_date(self, client):
        """Testa criação de tarefa com data de vencimento futura."""
        future_date = datetime.now() + timedelta(days=7)
        task_data = {"title": "Tarefa com prazo", "due_date": future_date.isoformat()}

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED

        created_task = response.json()
        assert "due_date" in created_task

    def test_create_task_with_past_due_date(self, client):
        """Testa criação de tarefa com data de vencimento passada."""
        past_date = datetime.now() - timedelta(days=7)
        task_data = {"title": "Tarefa atrasada", "due_date": past_date.isoformat()}

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == status.HTTP_201_CREATED

        created_task = response.json()
        assert "due_date" in created_task
