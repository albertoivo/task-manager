def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Task Manager API running..."}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "db_connected": True}
