from pathlib import Path

import pandas as pd
import pytest

from app.services.charts import (
    ChartResult,
    StaticChartResult,
    generate_automatic_chart_images,
    generate_automatic_charts,
    generate_categorical_bar_chart,
    generate_categorical_bar_chart_image,
    generate_category_metric_bar_chart,
    generate_numeric_histogram,
    generate_numeric_histogram_image,
    generate_scatter_chart,
    generate_time_series_chart,
)
from app.services.data_loader import load_spreadsheet

BENCHMARK_PATH = (
    Path(__file__).parent / "fixtures" / "databoard_autodetect_benchmark.xlsx"
)


def _create_mixed_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Categoria": ["A", "B", "A", "C"],
            "Valor": [10, 20, 30, 40],
        }
    )


def test_generate_categorical_bar_chart_returns_chart_result():
    dataframe = _create_mixed_dataframe()
    chart = generate_categorical_bar_chart(dataframe)

    assert isinstance(chart, ChartResult)
    assert chart.chart_type == "bar"
    assert chart.column_name == "Categoria"
    assert "plotly" in chart.html.lower()


def test_generate_numeric_histogram_returns_chart_result():
    dataframe = _create_mixed_dataframe()
    chart = generate_numeric_histogram(dataframe)

    assert isinstance(chart, ChartResult)
    assert chart.chart_type == "histogram"
    assert chart.column_name == "Valor"
    assert "plotly" in chart.html.lower()


def test_generate_automatic_charts_returns_available_charts():
    dataframe = _create_mixed_dataframe()
    charts = generate_automatic_charts(dataframe)

    assert len(charts) == 2
    assert any(chart.chart_type == "bar" for chart in charts)
    assert any(chart.chart_type == "histogram" for chart in charts)


def test_generate_automatic_charts_returns_empty_list_for_empty_dataframe():
    assert generate_automatic_charts(pd.DataFrame()) == []


def test_generate_automatic_charts_rejects_invalid_input():
    with pytest.raises(TypeError):
        generate_automatic_charts("invalid")


def test_generate_categorical_bar_chart_image_returns_png():
    chart = generate_categorical_bar_chart_image(_create_mixed_dataframe())

    assert isinstance(chart, StaticChartResult)
    assert chart.chart_type == "bar"
    assert chart.column_name == "Categoria"
    assert chart.image_bytes.startswith(b"\x89PNG\r\n\x1a\n")


def test_generate_numeric_histogram_image_returns_png():
    chart = generate_numeric_histogram_image(_create_mixed_dataframe())

    assert isinstance(chart, StaticChartResult)
    assert chart.chart_type == "histogram"
    assert chart.column_name == "Valor"
    assert chart.image_bytes.startswith(b"\x89PNG\r\n\x1a\n")


def test_generate_automatic_chart_images_returns_available_images():
    charts = generate_automatic_chart_images(_create_mixed_dataframe())

    assert len(charts) == 2
    assert all(isinstance(chart, StaticChartResult) for chart in charts)
    assert any(chart.chart_type == "bar" for chart in charts)
    assert any(chart.chart_type == "histogram" for chart in charts)
    assert all(chart.image_bytes.startswith(b"\x89PNG\r\n\x1a\n") for chart in charts)


def test_generate_automatic_chart_images_returns_empty_list_for_empty_dataframe():
    assert generate_automatic_chart_images(pd.DataFrame()) == []


def test_generate_automatic_chart_images_rejects_invalid_input():
    with pytest.raises(TypeError):
        generate_automatic_chart_images("invalid")


def test_numeric_histogram_ignores_numeric_identifier():
    dataframe = pd.DataFrame(
        {
            "CLIENTE_ID": [1001, 1002, 1003, 1004],
            "QUANTIDADE": [1, 2, 3, 4],
        }
    )

    chart = generate_numeric_histogram(dataframe)

    assert chart is not None
    assert chart.column_name == "QUANTIDADE"


def test_categorical_chart_does_not_use_identifier_or_free_text():
    dataframe = pd.DataFrame(
        {
            "PEDIDO_ID": ["P1", "P2", "P3"],
            "OBSERVACAO": [
                "Texto livre suficientemente longo número um",
                "Texto livre suficientemente longo número dois",
                "Texto livre suficientemente longo número três",
            ],
        }
    )

    assert generate_categorical_bar_chart(dataframe) is None


def test_category_metric_bar_uses_semantic_dimension_and_metric():
    dataframe = pd.DataFrame(
        {
            "REGIAO": ["Norte", "Sul", "Norte", "Sul"],
            "VALOR_TOTAL": [100.0, 200.0, 150.0, 250.0],
        }
    )

    chart = generate_category_metric_bar_chart(dataframe)

    assert chart is not None
    assert chart.chart_type == "bar"
    assert chart.column_name == "REGIAO"
    assert chart.metric_name == "VALOR_TOTAL"


def test_time_series_uses_date_and_metric():
    dataframe = pd.DataFrame(
        {
            "DATA": ["01/01/2026", "02/01/2026", "03/01/2026"],
            "RECEITA": [100.0, 200.0, 150.0],
        }
    )

    chart = generate_time_series_chart(dataframe)

    assert chart is not None
    assert chart.chart_type == "line"
    assert chart.column_name == "DATA"
    assert chart.metric_name == "RECEITA"


def test_scatter_requires_two_semantic_metrics():
    dataframe = pd.DataFrame(
        {
            "QUANTIDADE": [1, 2, 3, 4],
            "VALOR_TOTAL": [100.0, 200.0, 300.0, 400.0],
            "CLIENTE_ID": [1001, 1002, 1003, 1004],
        }
    )

    chart = generate_scatter_chart(dataframe)

    assert chart is not None
    assert chart.chart_type == "scatter"
    assert chart.column_name == "QUANTIDADE"
    assert chart.metric_name == "VALOR_TOTAL"


def test_currency_text_can_be_used_as_histogram_metric():
    dataframe = pd.DataFrame(
        {
            "FATURAMENTO": [
                "R$ 1.250,00",
                "R$ 980,50",
                "R$ 2.100,75",
            ]
        }
    )

    chart = generate_numeric_histogram(dataframe)

    assert chart is not None
    assert chart.column_name == "FATURAMENTO"


def test_high_cardinality_category_is_not_plotted_automatically():
    dataframe = pd.DataFrame(
        {
            "CATEGORIA": [f"Categoria {index}" for index in range(30)],
        }
    )

    assert generate_categorical_bar_chart(dataframe) is None
    assert generate_automatic_charts(dataframe) == []


def test_benchmark_automatic_charts_ignore_identifiers_and_prioritize_useful_views():
    dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    charts = generate_automatic_charts(dataframe)

    assert 1 <= len(charts) <= 3
    assert any(chart.chart_type == "line" for chart in charts)
    assert any(chart.chart_type == "bar" for chart in charts)
    assert any(chart.chart_type == "histogram" for chart in charts)

    used_columns = {
        value
        for chart in charts
        for value in (chart.column_name, chart.metric_name)
        if value is not None
    }

    assert "CLIENTE_ID" not in used_columns
    assert "PEDIDO_ID" not in used_columns
