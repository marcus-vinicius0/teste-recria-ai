from fastapi.testclient import TestClient
from app.main import app
import time
import uuid

client = TestClient(app)


def test_create_event():
    event_id = str(uuid.uuid4())

    response = client.post("/events", json={
        "event_id": event_id,
        "payload": {"a": 1}
    })

    assert response.status_code == 200

    data = response.json()

    assert data["event_id"] == event_id
    # aceita variação por causa do processamento assíncrono
    assert data["status"] in ["pending", "processing", "success"]
    assert "id" in data


def test_idempotency():
    event_id = str(uuid.uuid4())

    payload = {
        "event_id": event_id,
        "payload": {"a": 1}
    }

    r1 = client.post("/events", json=payload)
    r2 = client.post("/events", json=payload)

    assert r1.status_code == 200
    assert r2.status_code == 200

    data1 = r1.json()
    data2 = r2.json()

    # deve ser o mesmo registro (idempotência)
    assert data1["id"] == data2["id"]


def test_retry_and_failure(monkeypatch):
    # força a função a sempre falhar
    def always_fail():
        raise Exception("Erro forçado")

    monkeypatch.setattr(
        "app.services.event_processor.simulate_processing",
        always_fail
    )

    event_id = str(uuid.uuid4())

    response = client.post("/events", json={
        "event_id": event_id,
        "payload": {"a": 1}
    })

    assert response.status_code == 200

    created_event_id = response.json()["id"]

    # espera processamento terminar (retry + backoff)
    time.sleep(6)

    # busca eventos
    response = client.get("/events")
    data = response.json()["data"]

    # encontra o evento
    event = next(e for e in data if e["id"] == created_event_id)

    # valida resultado final
    assert event["status"] == "failed"