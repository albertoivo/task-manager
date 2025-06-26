import os
import sys
from pathlib import Path

# Definir ambiente de teste é a primeira coisa a se fazer
os.environ["TESTING"] = "True"

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import pytest
from fastapi.testclient import TestClient

from app.database import engine
from app.main import app
# Agora importamos o engine e a Base do módulo que já sabe sobre o ambiente de teste
from app.models.base import Base


@pytest.fixture(scope="function")
def client():
    # Cria as tabelas no banco de dados de teste (SQLite)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    # Limpa o banco de dados depois que o teste termina
    Base.metadata.drop_all(bind=engine)
