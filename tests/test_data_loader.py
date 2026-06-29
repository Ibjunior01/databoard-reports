import pandas as pd
import pytest

from app.services.data_loader import (
    UnsupportedFileTypeError,
    allowed_file,
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