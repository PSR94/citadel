def test_query_api_returns_grounded_response(client):
    response = client.post(
        "/api/v1/chat/query",
        json={"query": "What is the incident escalation policy for severity 1 outages?"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["answer"]
    assert payload["citations"]
    assert payload["debug"]["stage_timings_ms"]

