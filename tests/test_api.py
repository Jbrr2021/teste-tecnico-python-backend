from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app


def criar_cliente_temporario(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test_performance.db"))
    init_db()
    return TestClient(app)


def test_deve_criar_registro_foco(tmp_path, monkeypatch):
    client = criar_cliente_temporario(tmp_path, monkeypatch)

    response = client.post(
        "/registro-foco",
        json={
            "nivel_foco": 5,
            "tempo_minutos": 90,
            "comentario": "Estudei FastAPI e finalizei o endpoint principal.",
            "categoria": "estudo",
            "tags": ["python", "api"],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["nivel_foco"] == 5
    assert body["tags"] == ["python", "api"]


def test_deve_rejeitar_nivel_foco_invalido(tmp_path, monkeypatch):
    client = criar_cliente_temporario(tmp_path, monkeypatch)

    response = client.post(
        "/registro-foco",
        json={
            "nivel_foco": 6,
            "tempo_minutos": 45,
            "comentario": "Teste com nível inválido.",
        },
    )

    assert response.status_code == 422


def test_deve_rejeitar_comentario_vazio(tmp_path, monkeypatch):
    client = criar_cliente_temporario(tmp_path, monkeypatch)

    response = client.post(
        "/registro-foco",
        json={
            "nivel_foco": 3,
            "tempo_minutos": 30,
            "comentario": "",
        },
    )

    assert response.status_code == 422


def test_deve_rejeitar_tempo_minutos_invalido(tmp_path, monkeypatch):
    client = criar_cliente_temporario(tmp_path, monkeypatch)

    response = client.post(
        "/registro-foco",
        json={
            "nivel_foco": 4,
            "tempo_minutos": 0,
            "comentario": "Sessão com tempo inválido.",
        },
    )

    assert response.status_code == 422


def test_deve_gerar_diagnostico(tmp_path, monkeypatch):
    client = criar_cliente_temporario(tmp_path, monkeypatch)

    client.post(
        "/registro-foco",
        json={
            "nivel_foco": 5,
            "tempo_minutos": 60,
            "comentario": "Codando sem notificações.",
            "categoria": "coding",
        },
    )
    client.post(
        "/registro-foco",
        json={
            "nivel_foco": 3,
            "tempo_minutos": 30,
            "comentario": "Estudo com algumas distrações no WhatsApp.",
            "categoria": "estudo",
        },
    )

    response = client.get("/diagnostico-produtividade")

    assert response.status_code == 200
    body = response.json()
    assert body["total_registros"] == 2
    assert body["media_nivel_foco"] == 4.0
    assert body["tempo_total_focado"] == 90
    assert body["tempo_total_formatado"] == "1h 30min"
    assert body["insight_comentarios"] is not None


def test_diagnostico_sem_registros(tmp_path, monkeypatch):
    client = criar_cliente_temporario(tmp_path, monkeypatch)

    response = client.get("/diagnostico-produtividade")

    assert response.status_code == 200
    body = response.json()
    assert body["total_registros"] == 0
    assert body["media_nivel_foco"] == 0
    assert body["tempo_total_focado"] == 0
    assert body["mensagem_feedback"] == "Ainda não há registros. Faça seu primeiro bloco de foco para gerar um diagnóstico."
