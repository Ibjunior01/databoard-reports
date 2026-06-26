from app import create_app


def test_index_route_returns_success():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"DataBoard Reports" in response.data