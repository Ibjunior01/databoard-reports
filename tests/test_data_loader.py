from pathlib import Path

import pandas as pd
import pytest

from app.services.data_loader import (
    InvalidSpreadsheetError,
    UnsupportedFileTypeError,
    allowed_file,
    detect_header_row,
    load_spreadsheet,
    load_spreadsheet_metadata,
)


def test_allowed_file_accepts_supported_extensions():
    assert allowed_file("sales.csv") is True
    assert allowed_file("sales.xlsx") is True
    assert allowed_file("sales.xls") is True


def test_allowed_file_rejects_unsupported_extensions():
    assert allowed_file("document.pdf") is False
    assert allowed_file("image.png") is False
    assert allowed_file("notes.txt") is False
    assert allowed_file("") is False


def test_load_csv_file(tmp_path):
    csv_path = tmp_path / "sales.csv"

    dataframe = pd.DataFrame(
        {
            "product": ["Notebook", "Mouse", "Keyboard"],
            "quantity": [2, 10, 5],
            "revenue": [7000.00, 500.00, 750.00],
        }
    )

    dataframe.to_csv(csv_path, index=False)

    loaded_dataframe = load_spreadsheet(csv_path)

    assert loaded_dataframe.shape == (3, 3)
    assert list(loaded_dataframe.columns) == ["product", "quantity", "revenue"]
    assert loaded_dataframe.iloc[0]["product"] == "Notebook"


def test_load_excel_file(tmp_path):
    excel_path = tmp_path / "sales.xlsx"

    dataframe = pd.DataFrame(
        {
            "product": ["Notebook", "Mouse", "Keyboard"],
            "quantity": [2, 10, 5],
            "revenue": [7000.00, 500.00, 750.00],
        }
    )

    dataframe.to_excel(excel_path, index=False)

    loaded_dataframe = load_spreadsheet(excel_path)

    assert loaded_dataframe.shape == (3, 3)
    assert list(loaded_dataframe.columns) == ["product", "quantity", "revenue"]
    assert loaded_dataframe.iloc[1]["product"] == "Mouse"


def test_load_spreadsheet_metadata_from_csv(tmp_path):
    csv_path = tmp_path / "sales.csv"

    dataframe = pd.DataFrame(
        {
            "product": ["Notebook", "Mouse", "Keyboard"],
            "quantity": [2, 10, 5],
            "revenue": [7000.00, 500.00, 750.00],
        }
    )

    dataframe.to_csv(csv_path, index=False)

    metadata = load_spreadsheet_metadata(csv_path)

    assert metadata["file_name"] == "sales.csv"
    assert metadata["file_extension"] == ".csv"
    assert metadata["rows"] == 3
    assert metadata["columns"] == 3
    assert metadata["column_names"] == ["product", "quantity", "revenue"]
    assert len(metadata["preview"]) == 3
    assert metadata["preview"][0]["product"] == "Notebook"


def test_load_spreadsheet_metadata_from_excel(tmp_path):
    excel_path = tmp_path / "sales.xlsx"

    dataframe = pd.DataFrame(
        {
            "product": ["Notebook", "Mouse", "Keyboard"],
            "quantity": [2, 10, 5],
            "revenue": [7000.00, 500.00, 750.00],
        }
    )

    dataframe.to_excel(excel_path, index=False)

    metadata = load_spreadsheet_metadata(excel_path, preview_rows=2)

    assert metadata["file_name"] == "sales.xlsx"
    assert metadata["file_extension"] == ".xlsx"
    assert metadata["rows"] == 3
    assert metadata["columns"] == 3
    assert metadata["column_names"] == ["product", "quantity", "revenue"]
    assert len(metadata["preview"]) == 2
    assert metadata["preview"][1]["product"] == "Mouse"


def test_load_spreadsheet_raises_error_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_spreadsheet(missing_file)


def test_load_spreadsheet_raises_error_for_unsupported_extension(tmp_path):
    unsupported_file = tmp_path / "report.pdf"
    unsupported_file.write_text("fake pdf content", encoding="utf-8")

    with pytest.raises(UnsupportedFileTypeError):
        load_spreadsheet(unsupported_file)


def test_load_spreadsheet_metadata_respects_preview_rows(tmp_path):
    csv_path = tmp_path / "sales.csv"

    dataframe = pd.DataFrame(
        {
            "product": ["A", "B", "C", "D", "E", "F"],
            "quantity": [1, 2, 3, 4, 5, 6],
        }
    )

    dataframe.to_csv(csv_path, index=False)

    metadata = load_spreadsheet_metadata(csv_path, preview_rows=3)

    assert metadata["rows"] == 6
    assert len(metadata["preview"]) == 3
    assert metadata["preview"][2]["product"] == "C"


def test_load_spreadsheet_raises_invalid_error_for_corrupted_xlsx(
    tmp_path,
):
    excel_path = tmp_path / "corrupted.xlsx"
    excel_path.write_bytes(b"this is not a valid Excel workbook")

    with pytest.raises(InvalidSpreadsheetError):
        load_spreadsheet(excel_path)


def test_load_spreadsheet_raises_invalid_error_for_invalid_csv_encoding(
    tmp_path,
):
    csv_path = tmp_path / "invalid.csv"
    csv_path.write_bytes(b"\xff\xfe\x00\x00\xff\xfe")

    with pytest.raises(InvalidSpreadsheetError):
        load_spreadsheet(csv_path)


def test_detect_header_row_when_header_is_not_first_row():
    dataframe = pd.DataFrame(
        [
            [
                "RELATÓRIO COMERCIAL",
                None,
                None,
                None,
            ],
            [
                "Período: janeiro a agosto",
                None,
                None,
                None,
            ],
            [
                "DATA",
                "UNIDADE",
                "SERVICO",
                "RECEITA",
            ],
            [
                "01/01/2026",
                "Aldeota",
                "Consultoria",
                1000,
            ],
            [
                "02/01/2026",
                "Eusébio",
                "Suporte",
                800,
            ],
        ]
    )

    detected_row = detect_header_row(dataframe)

    assert detected_row == 2


def test_detect_header_row_keeps_first_row_for_standard_table():
    dataframe = pd.DataFrame(
        [
            [
                "DATA",
                "PRODUTO",
                "VALOR",
                "CLIENTE",
            ],
            [
                "01/01/2026",
                "Notebook",
                3500,
                "Cliente A",
            ],
            [
                "02/01/2026",
                "Monitor",
                1200,
                "Cliente B",
            ],
        ]
    )

    detected_row = detect_header_row(dataframe)

    assert detected_row == 0


def test_load_spreadsheet_detects_excel_header_on_third_row(
    tmp_path,
):
    excel_path = tmp_path / "header_linha_3.xlsx"

    raw_dataframe = pd.DataFrame(
        [
            [
                "RELATÓRIO COMERCIAL — TESTE",
                None,
                None,
                None,
                None,
                None,
            ],
            [
                "Período: janeiro a agosto de 2026",
                None,
                None,
                None,
                None,
                None,
            ],
            [
                "DATA",
                "UNIDADE",
                "SERVICO",
                "QTD",
                "RECEITA",
                "STATUS",
            ],
            [
                "01/01/2026",
                "Aldeota",
                "Consultoria",
                2,
                1000,
                "Concluído",
            ],
            [
                "02/01/2026",
                "Eusébio",
                "Suporte",
                1,
                800,
                "Pendente",
            ],
        ]
    )

    raw_dataframe.to_excel(
        excel_path,
        index=False,
        header=False,
    )

    dataframe = load_spreadsheet(excel_path)

    assert list(dataframe.columns) == [
        "DATA",
        "UNIDADE",
        "SERVICO",
        "QTD",
        "RECEITA",
        "STATUS",
    ]

    assert len(dataframe) == 2


BENCHMARK_PATH = (
    Path(__file__).parent / "fixtures" / "databoard_autodetect_benchmark.xlsx"
)


@pytest.mark.parametrize(
    (
        "sheet_name",
        "expected_rows",
        "expected_columns",
    ),
    [
        (
            "01_Base_Realista",
            240,
            [
                "VENDEDOR",
                "CLIENTE_ID",
                "DATA_VENDA",
                "REGIAO",
                "VALOR_TOTAL",
                "PEDIDO_ID",
                "QUANTIDADE",
                "PRODUTO",
                "MARGEM_PCT",
                "ATIVO",
            ],
        ),
        (
            "02_Colunas_Reordenadas",
            120,
            [
                "PRODUTO",
                "ATIVO",
                "PEDIDO_ID",
                "MARGEM_PCT",
                "QUANTIDADE",
                "REGIAO",
                "CLIENTE_ID",
                "VALOR_TOTAL",
                "VENDEDOR",
                "DATA_VENDA",
            ],
        ),
        (
            "03_Tipos_Desafiadores",
            80,
            [
                "CODIGO_CLIENTE",
                "DATA",
                "FATURAMENTO",
                "DESCONTO",
                "CATEGORIA",
                "CEP",
                "OBSERVACAO",
            ],
        ),
        (
            "04_Cabecalho_Linha3",
            100,
            [
                "DATA",
                "UNIDADE",
                "SERVICO",
                "QTD",
                "RECEITA",
                "STATUS",
            ],
        ),
    ],
)
def test_benchmark_sheets_load_with_expected_structure(
    sheet_name,
    expected_rows,
    expected_columns,
):
    dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name=sheet_name,
    )

    assert len(dataframe) == expected_rows
    assert list(dataframe.columns) == expected_columns


def test_benchmark_reordered_columns_preserve_same_schema():
    base_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    reordered_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="02_Colunas_Reordenadas",
    )

    assert set(base_dataframe.columns) == set(reordered_dataframe.columns)

    assert list(base_dataframe.columns) != list(reordered_dataframe.columns)
