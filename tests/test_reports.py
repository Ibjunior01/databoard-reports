import base64
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from app.services.analyzer import analyze_dataframe
from app.services.charts import StaticChartResult
from app.services.reports import (
    _build_analysis_summary,
    _build_dataframe_preview,
    _build_numeric_statistics,
    _format_number,
    _format_preview_value,
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
        created_at=created_at
        or datetime(
            2026,
            7,
            13,
            10,
            30,
            0,
        ),
    )


def _create_analysis_result():
    """
    Cria uma análise automática contendo colunas numéricas,
    categóricas e valores ausentes.
    """

    dataframe = pd.DataFrame(
        {
            "categoria": [
                "A",
                "B",
                None,
            ],
            "valor": [
                10,
                20,
                None,
            ],
        }
    )

    return analyze_dataframe(
        dataframe
    )


def _create_test_png_bytes() -> bytes:
    """
    Retorna uma pequena imagem PNG válida em memória.

    O teste do serviço de relatórios não precisa executar
    novamente o Plotly/Kaleido, pois essa integração já é
    validada em tests/test_charts.py.
    """

    png_base64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"
        "CAQAAAC1HAwCAAAAC0lEQVR42mNk"
        "YAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    )

    return base64.b64decode(
        png_base64
    )


def _create_static_chart_result() -> StaticChartResult:
    """
    Cria um gráfico estático simulado para os testes do PDF.
    """

    return StaticChartResult(
        title="Distribuição por categoria",
        chart_type="bar",
        column_name="categoria",
        image_bytes=_create_test_png_bytes(),
    )


def test_generate_upload_report_creates_pdf(
    tmp_path,
):
    upload_record = _create_upload_record()
    analysis_result = _create_analysis_result()

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
    )

    assert isinstance(
        report_path,
        Path,
    )

    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.suffix == ".pdf"
    assert report_path.stat().st_size > 0


def test_generate_upload_report_creates_valid_pdf_header(
    tmp_path,
):
    upload_record = _create_upload_record(
        record_id=2,
        file_name=(
            "relatorio financeiro.xlsx"
        ),
        file_extension=".xlsx",
        row_count=250,
        column_count=12,
        created_at=datetime(
            2026,
            7,
            13,
            11,
            0,
            0,
        ),
    )

    analysis_result = (
        _create_analysis_result()
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
    )

    with report_path.open(
        "rb"
    ) as pdf_file:
        pdf_header = pdf_file.read(4)

    assert pdf_header == b"%PDF"


def test_generate_upload_report_creates_reports_directory(
    tmp_path,
):
    reports_folder = (
        tmp_path
        / "generated_reports"
    )

    upload_record = _create_upload_record(
        record_id=3,
        file_name="clientes.xls",
        file_extension=".xls",
        row_count=50,
        column_count=8,
        created_at=None,
    )

    analysis_result = (
        _create_analysis_result()
    )

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
            "categoria": [
                "A",
                "B",
                None,
            ],
            "valor": [
                10,
                20,
                None,
            ],
            "ativo": [
                True,
                False,
                True,
            ],
        }
    )

    analysis_result = (
        analyze_dataframe(
            dataframe
        )
    )

    summary = (
        _build_analysis_summary(
            analysis_result
        )
    )

    assert (
        summary[
            "numeric_columns"
        ]
        == ["valor"]
    )

    assert (
        summary[
            "numeric_columns_count"
        ]
        == 1
    )

    assert (
        summary[
            "categorical_columns"
        ]
        == [
            "categoria",
            "ativo",
        ]
    )

    assert (
        summary[
            "categorical_columns_count"
        ]
        == 2
    )

    assert (
        summary[
            "total_missing_values"
        ]
        == 2
    )

    missing_by_column = {
        item["column"]: item
        for item in summary[
            "missing_columns"
        ]
    }

    assert (
        missing_by_column[
            "categoria"
        ]["count"]
        == 1
    )

    assert (
        missing_by_column[
            "categoria"
        ]["percent"]
        == 33.33
    )

    assert (
        missing_by_column[
            "valor"
        ]["count"]
        == 1
    )

    assert (
        missing_by_column[
            "valor"
        ]["percent"]
        == 33.33
    )


def test_build_analysis_summary_handles_dataframe_without_missing_values():
    dataframe = pd.DataFrame(
        {
            "produto": [
                "A",
                "B",
            ],
            "quantidade": [
                10,
                20,
            ],
        }
    )

    analysis_result = (
        analyze_dataframe(
            dataframe
        )
    )

    summary = (
        _build_analysis_summary(
            analysis_result
        )
    )

    assert (
        summary[
            "numeric_columns"
        ]
        == ["quantidade"]
    )

    assert (
        summary[
            "categorical_columns"
        ]
        == ["produto"]
    )

    assert (
        summary[
            "total_missing_values"
        ]
        == 0
    )

    assert (
        summary[
            "missing_columns"
        ]
        == []
    )


def test_format_number_formats_integer_values():
    assert (
        _format_number(1000)
        == "1.000"
    )

    assert (
        _format_number(25.0)
        == "25"
    )


def test_format_number_formats_decimal_values():
    assert (
        _format_number(1234.5)
        == "1.234,50"
    )

    assert (
        _format_number(10.333333)
        == "10,33"
    )


def test_format_number_handles_none():
    assert (
        _format_number(None)
        == "Não disponível"
    )


def test_build_numeric_statistics_returns_formatted_values():
    dataframe = pd.DataFrame(
        {
            "valor": [
                10,
                20,
                30,
            ],
            "quantidade": [
                2,
                4,
                6,
            ],
            "categoria": [
                "A",
                "B",
                "C",
            ],
        }
    )

    analysis_result = (
        analyze_dataframe(
            dataframe
        )
    )

    statistics = (
        _build_numeric_statistics(
            analysis_result
        )
    )

    statistics_by_column = {
        item["column"]: item
        for item in statistics
    }

    assert (
        statistics_by_column[
            "valor"
        ]
        == {
            "column": "valor",
            "mean": "20",
            "median": "20",
            "min": "10",
            "max": "30",
        }
    )

    assert (
        statistics_by_column[
            "quantidade"
        ]
        == {
            "column": "quantidade",
            "mean": "4",
            "median": "4",
            "min": "2",
            "max": "6",
        }
    )


def test_build_numeric_statistics_handles_dataframe_without_numeric_columns():
    dataframe = pd.DataFrame(
        {
            "produto": [
                "A",
                "B",
                "C",
            ],
            "categoria": [
                "X",
                "Y",
                "Z",
            ],
        }
    )

    analysis_result = (
        analyze_dataframe(
            dataframe
        )
    )

    statistics = (
        _build_numeric_statistics(
            analysis_result
        )
    )

    assert statistics == []


def test_generate_upload_report_without_numeric_columns(
    tmp_path,
):
    upload_record = _create_upload_record(
        record_id=4,
        file_name="categorias.csv",
        file_extension=".csv",
        row_count=3,
        column_count=2,
    )

    dataframe = pd.DataFrame(
        {
            "produto": [
                "A",
                "B",
                "C",
            ],
            "categoria": [
                "X",
                "Y",
                "Z",
            ],
        }
    )

    analysis_result = (
        analyze_dataframe(
            dataframe
        )
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
    )

    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.suffix == ".pdf"
    assert report_path.stat().st_size > 0


def test_generate_upload_report_with_static_chart(
    tmp_path,
):
    upload_record = _create_upload_record(
        record_id=5,
    )

    analysis_result = (
        _create_analysis_result()
    )

    chart_result = (
        _create_static_chart_result()
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
        chart_results=[
            chart_result
        ],
    )

    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.suffix == ".pdf"
    assert report_path.stat().st_size > 0

    with report_path.open(
        "rb"
    ) as pdf_file:
        assert (
            pdf_file.read(4)
            == b"%PDF"
        )


def test_generate_upload_report_accepts_multiple_static_charts(
    tmp_path,
):
    upload_record = _create_upload_record(
        record_id=6,
    )

    analysis_result = (
        _create_analysis_result()
    )

    bar_chart = StaticChartResult(
        title="Distribuição por categoria",
        chart_type="bar",
        column_name="categoria",
        image_bytes=_create_test_png_bytes(),
    )

    histogram = StaticChartResult(
        title="Distribuição de valor",
        chart_type="histogram",
        column_name="valor",
        image_bytes=_create_test_png_bytes(),
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
        chart_results=[
            bar_chart,
            histogram,
        ],
    )

    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.stat().st_size > 0

    with report_path.open(
        "rb"
    ) as pdf_file:
        assert (
            pdf_file.read(4)
            == b"%PDF"
        )


def test_format_preview_value_handles_missing_and_regular_values():
    assert _format_preview_value(None) == "-"
    assert _format_preview_value(pd.NA) == "-"
    assert _format_preview_value("Produto A") == "Produto A"
    assert _format_preview_value(25) == "25"


def test_format_preview_value_truncates_long_text():
    value = "abcdefghijklm"

    formatted_value = _format_preview_value(
        value,
        max_length=10,
    )

    assert formatted_value == "abcdefg..."
    assert len(formatted_value) == 10


def test_build_dataframe_preview_limits_rows_and_columns():
    dataframe = pd.DataFrame(
        {
            "coluna_1": [1, 2, 3, 4],
            "coluna_2": ["A", "B", "C", "D"],
            "coluna_3": [10, 20, 30, 40],
            "coluna_4": ["X", "Y", "Z", "W"],
        }
    )

    preview = _build_dataframe_preview(
        dataframe,
        max_rows=2,
        max_columns=3,
    )

    assert preview["columns"] == [
        "coluna_1",
        "coluna_2",
        "coluna_3",
    ]

    assert preview["rows"] == [
        ["1", "A", "10"],
        ["2", "B", "20"],
    ]

    assert preview["total_rows"] == 4
    assert preview["total_columns"] == 4
    assert preview["displayed_rows"] == 2
    assert preview["displayed_columns"] == 3
    assert preview["omitted_rows"] == 2
    assert preview["omitted_columns"] == 1


def test_build_dataframe_preview_formats_missing_values():
    dataframe = pd.DataFrame(
        {
            "produto": [
                "A",
                None,
            ],
            "valor": [
                10,
                None,
            ],
        }
    )

    preview = _build_dataframe_preview(
        dataframe
    )

    assert preview["rows"] == [
        ["A", "10.0"],
        ["-", "-"],
    ]


def test_build_dataframe_preview_rejects_invalid_input():
    with pytest.raises(TypeError):
        _build_dataframe_preview(
            "invalid"
        )


def test_generate_upload_report_with_dataframe_preview(
    tmp_path,
):
    upload_record = _create_upload_record(
        record_id=7,
        file_name="preview.csv",
        file_extension=".csv",
        row_count=3,
        column_count=3,
    )

    dataframe = pd.DataFrame(
        {
            "produto": [
                "Café",
                "Salgado",
                "Suco",
            ],
            "categoria": [
                "Bebida",
                "Lanche",
                "Bebida",
            ],
            "valor": [
                8.5,
                7.0,
                6.5,
            ],
        }
    )

    analysis_result = analyze_dataframe(
        dataframe
    )

    report_path = generate_upload_report(
        upload_record=upload_record,
        analysis_result=analysis_result,
        reports_folder=tmp_path,
        dataframe=dataframe,
    )

    assert report_path.exists()
    assert report_path.is_file()
    assert report_path.suffix == ".pdf"
    assert report_path.stat().st_size > 0

    with report_path.open(
        "rb"
    ) as pdf_file:
        assert pdf_file.read(4) == b"%PDF"