from fastapi.testclient import TestClient

from lumen.api import create_app


def test_health(container):
    client = TestClient(create_app(container))
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_chat(container):
    client = TestClient(create_app(container))
    r = client.post("/chat", json={"message": "hi"})
    assert r.status_code == 200
    assert r.json()["reply"] == "42"


def test_agent_run_endpoint(container):
    client = TestClient(create_app(container))
    r = client.post("/agent/run", json={"question": "q"})
    assert r.status_code == 200
    assert isinstance(r.json()["answer"], str)


def test_metrics_endpoint(container):
    client = TestClient(create_app(container))
    r = client.get("/metrics")
    assert r.status_code == 200
    body = r.json()
    assert "calls" in body
    assert "per_module" in body
