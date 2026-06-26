from app.routes import allowed_file


def test_allowed_file_accepts_csv():
    assert allowed_file("dados.csv") is True


def test_allowed_file_accepts_xlsx():
    assert allowed_file("relatorio.xlsx") is True


def test_allowed_file_accepts_xls():
    assert allowed_file("planilha.xls") is True


def test_allowed_file_rejects_txt():
    assert allowed_file("documento.txt") is False


def test_allowed_file_rejects_pdf():
    assert allowed_file("relatorio.pdf") is False


def test_allowed_file_rejects_png():
    assert allowed_file("imagem.png") is False


def test_allowed_file_rejects_file_without_extension():
    assert allowed_file("arquivo_sem_extensao") is False