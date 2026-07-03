from io import BytesIO


def test_upload_displays_automatic_charts(client):
    data = {
        "file": (
            BytesIO(b"Categoria,Valor\nA,10\nB,20\nA,30\nC,40\n"),
            "dados.csv",
        )
    }

    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Gráficos automáticos".encode("utf-8") in response.data
    assert b"plotly" in response.data.lower()