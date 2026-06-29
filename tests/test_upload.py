# from app.routes import allowed_file


# def test_allowed_file_accepts_csv():
#     assert allowed_file("dados.csv") is True


# def test_allowed_file_accepts_xlsx():
#     assert allowed_file("relatorio.xlsx") is True


# def test_allowed_file_accepts_xls():
#     assert allowed_file("planilha.xls") is True


# def test_allowed_file_rejects_txt():
#     assert allowed_file("documento.txt") is False


# def test_allowed_file_rejects_pdf():
#     assert allowed_file("relatorio.pdf") is False


# def test_allowed_file_rejects_png():
#     assert allowed_file("imagem.png") is False


# def test_allowed_file_rejects_file_without_extension():
#     assert allowed_file("arquivo_sem_extensao") is False

from io import BytesIO


def test_upload_valid_csv_displays_metadata_preview(client):
    data = {
        "file": (
            BytesIO(b"produto,quantidade,valor\nNotebook,2,3500\nMouse,10,80\n"),
            "sales.csv",
        )
    }

    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"sales.csv" in response.data
    assert b"Linhas" in response.data
    assert b"Colunas" in response.data
    assert b"produto" in response.data
    assert b"quantidade" in response.data
    assert b"Notebook" in response.data
    assert b"Mouse" in response.data