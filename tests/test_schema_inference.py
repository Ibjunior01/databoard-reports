import pytest

from app.services.schema_inference import normalize_column_name


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        ("Valor Total", "VALOR_TOTAL"),
        (" valor_total ", "VALOR_TOTAL"),
        ("VALOR-TOTAL", "VALOR_TOTAL"),
        ("Código Cliente", "CODIGO_CLIENTE"),
        ("DATA_VENDA", "DATA_VENDA"),
        ("data venda", "DATA_VENDA"),
        ("Margem %", "MARGEM"),
        ("Observação", "OBSERVACAO"),
        ("  Produto   Principal  ", "PRODUTO_PRINCIPAL"),
        ("", ""),
        (None, ""),
    ],
)
def test_normalize_column_name(
    original,
    expected,
):
    assert normalize_column_name(original) == expected
