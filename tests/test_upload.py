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


def test_upload_displays_automatic_analysis(client):
    csv_content = b"produto,categoria,valor\nNotebook,Eletronicos,3500\nMouse,Eletronicos,120\nCadeira,Moveis,800\n"

    response = client.post(
        "/upload",
        data={
            "file": (BytesIO(csv_content), "analysis_test.csv"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"An\xc3\xa1lise autom\xc3\xa1tica" in response.data
    assert b"Colunas num\xc3\xa9ricas" in response.data
    assert b"Colunas categ\xc3\xb3ricas" in response.data
    assert b"Estat\xc3\xadsticas num\xc3\xa9ricas" in response.data
    assert b"valor" in response.data
    assert b"produto" in response.data