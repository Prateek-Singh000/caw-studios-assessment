import pytest
from fastapi.testclient import TestClient
from main import app, db, analytics_db, processed_job_ids

@pytest.fixture(autouse=True)
def clear_state():
    # THE FIX: Isolate test state before every test
    db.clear()
    analytics_db.clear()
    processed_job_ids.clear()
    yield

client = TestClient(app)

def test_pollute_state():
    db["stale-id"] = {"id": "stale-id", "short_code": "ex1", "long_url": "https://polluted.com", "principal_id": "principal_A"}
    assert "stale-id" in db

def test_create_link_conflict():
    # Because state is cleared, stale-id is gone and len(db) will correctly be 1
    res = client.post(
        "/api/links",
        json={"long_url": "https://example.com", "short_code": "ex1", "tags": ["test"]},
        headers={"X-API-Key": "key_alpha"}
    )
    assert res.status_code == 200
    assert len(db) == 1 # Passes cleanly!
