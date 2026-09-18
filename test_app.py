from app import app


def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "healthy"


def test_api_pool():
    client = app.test_client()
    res = client.get("/api/pool")
    assert res.status_code == 200
    assert res.get_json()["currency"] == "USD"


def test_apply_dti_exceeded():
    client = app.test_client()
    res = client.post(
        "/apply",
        data={
            "name": "Test User",
            "income": "5000",
            "debt": "2500",
            "amount": "1000",
        },
    )
    assert res.status_code == 200
    assert b"exceeds maximum underwriting tolerance" in res.data
