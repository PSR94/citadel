def test_health_endpoints(client):
    health = client.get("/health")
    readiness = client.get("/health/readiness")

    assert health.status_code == 200
    assert readiness.status_code == 200
    assert readiness.json()["documents"] >= 1

