from app import app, loans


def get_client():
    app.config["TESTING"] = True
    loans.clear()
    return app.test_client()


def test_health():
    client = get_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"


def test_valid_loan_approval():
    client = get_client()
    payload = {
        "borrower": "CleanTech Solutions",
        "amount": "10000",
        "income": "100000",
        "debt": "20000",
    }
    res = client.post("/apply", data=payload, follow_redirects=True)
    assert res.status_code == 200
    assert b"CleanTech Solutions" in res.data

    api_res = client.get("/api/loans")
    assert api_res.status_code == 200
    assert api_res.json["current_pool"] == 40000.0


def test_invalid_input_rejected():
    client = get_client()
    res = client.post("/apply", data={"borrower": "Incomplete Data"})
    assert res.status_code == 400


def test_high_dti_rejected():
    client = get_client()
    payload = {
        "borrower": "High Debt Corp",
        "amount": "5000",
        "income": "50000",
        "debt": "30000",
    }
    res = client.post("/apply", data=payload)
    assert res.status_code == 400
    assert b"exceeds the 40% threshold" in res.data


def test_liquidity_exceeded():
    client = get_client()
    payload = {
        "borrower": "Mega Project",
        "amount": "60000",
        "income": "200000",
        "debt": "10000",
    }
    res = client.post("/apply", data=payload)
    assert res.status_code == 400
