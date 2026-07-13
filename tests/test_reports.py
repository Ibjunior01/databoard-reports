from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

from app.services.analyzer import analyze_dataframe
from app.services.reports import (
    _build_analysis_summary,
    generate_upload_report,
)


def _create_upload_record(
    record_id: int = 1,
    file_name: str = "vendas.csv",
    file_extension: str = ".csv",
    row_count: int = 3,
    column_count: int = 2,
    created_at: datetime | None = None,
) -> SimpleNamespace:
    """
    Cria um registro simples de upload para os testes do relatório.
    """

    return SimpleNamespace(
        id=record_id,
        file_name=file_name,
        file_extension=file_extension,
        row_count=row_count,
        column_count=column_count,
        created_at=created_at or datetime(2026, 7, 13, 10, 30, 0),
    )


def _create_analysis_result():
    """
    Cria uma análise automática contendo colunas numéricas,
    categóricas e valores ausentes.
    """

    dataframe = pd.DataFrame(
        {
            "categoria": ["A", "B", None],
            "valor": [10, 20, None],
        }
    )

    return analyze_dataframe(dataframe)


def test_generate_upload_report_creates_pdf(tmp_path):
    upload_record = _create_upload_record()
    analysis_result = _create_analysis_result()

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
    )

    assert isinstance(report_path, Path)
    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.suffix == ".pdf"
    assert report_path.stat().st_size > 0


def test_generate_upload_report_creates_valid_pdf_header(tmp_path):
    upload_record = _create_upload_record(
        record_id=2,
        file_name="relatorio financeiro.xlsx",
        file_extension=".xlsx",
        row_count=250,
        column_count=12,
        created_at=datetime(2026, 7, 13, 11, 0, 0),
    )

    analysis_result = _create_analysis_result()

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
    )

    with report_path.open("rb") as pdf_file:
        pdf_header = pdf_file.read(4)

    assert pdf_header == b"%PDF"


def test_generate_upload_report_creates_reports_directory(tmp_path):
    reports_folder = tmp_path / "generated_reports"

    upload_record = _create_upload_record(
        record_id=3,
        file_name="clientes.xls",
        file_extension=".xls",
        row_count=50,
        column_count=8,
        created_at=None,
    )

    analysis_result = _create_analysis_result()

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=reports_folder,
    )

    assert reports_folder.exists()
    assert reports_folder.is_dir()
    assert report_path.exists()


def test_build_analysis_summary_returns_expected_values():
    dataframe = pd.DataFrame(
        {
            "categoria": ["A", "B", None],
            "valor": [10, 20, None],
            "ativo": [True, False, True],
        }
    )

    analysis_result = analyze_dataframe(dataframe)

    summary = _build_analysis_summary(analysis_result)

    assert summary["numeric_columns"] == ["valor"]
    assert summary["numeric_columns_count"] == 1

    assert summary["categorical_columns"] == [
        "categoria",
        "ativo",
    ]
    assert summary["categorical_columns_count"] == 2

    assert summary["total_missing_values"] == 2

    missing_by_column = {
        item["column"]: item
        for item in summary["missing_columns"]
    }

    assert missing_by_column["categoria"]["count"] == 1
    assert missing_by_column["categoria"]["percent"] == 33.33

    assert missing_by_column["valor"]["count"] == 1
    assert missing_by_column["valor"]["percent"] == 33.33


def test_build_analysis_summary_handles_dataframe_without_missing_values():
    dataframe = pd.DataFrame(
        {
            "produto": ["A", "B"],
            "quantidade": [10, 20],
        }
    )

    analysis_result = analyze_dataframe(dataframe)

    summary = _build_analysis_summary(analysis_result)

    assert summary["numeric_columns"] == ["quantidade"]
    assert summary["categorical_columns"] == ["produto"]
    assert summary["total_missing_values"] == 0
    assert summary["missing_columns"] == []