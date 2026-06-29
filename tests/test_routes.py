from io import BytesIO

import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app()
    app.config.update(
        TESTING=True,
        UPLOAD_FOLDER=tmp_path,
    )

    with app.test_client() as test_client:
        yield test_client


def test_index_route_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200


def test_upload_route_returns_200(client):
    response = client.get("/upload")

    assert response.status_code == 200
    assert "Upload" in response.get_data(as_text=True)


def test_upload_valid_csv_returns_success_message(client):
    data = {
        "file": (BytesIO(b"produto,valor\nCafe,10\n"), "vendas.csv")
    }

    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    page_content = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Arquivo carregado com sucesso" in page_content
    assert "vendas.csv" in page_content
    assert "produto" in page_content
    assert "Cafe" in page_content


def test_upload_invalid_pdf_returns_error_message(client):
    data = {
        "file": (BytesIO(b"conteudo fake"), "arquivo.pdf")
    }

    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    page_content = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Tipo de arquivo não permitido" in page_content