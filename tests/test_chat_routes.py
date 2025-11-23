def test_send_and_summary(client):
    r = client.post("/api/send", json={"text":"I am happy"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["status"] == "ok"
    r2 = client.get("/api/summary")
    assert r2.status_code == 200
    s = r2.get_json()
    assert s["count"] >= 1
