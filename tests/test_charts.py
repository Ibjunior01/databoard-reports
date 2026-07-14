import pandas as pd
import pytest

from app.services.charts import (
    ChartResult,
    StaticChartResult,
    generate_automatic_chart_images,
    generate_automatic_charts,
    generate_categorical_bar_chart,
    generate_categorical_bar_chart_image,
    generate_numeric_histogram,
    generate_numeric_histogram_image,
)


def _create_mixed_dataframe() -> pd.DataFrame:
    """
    Cria um DataFrame com dados categóricos e numéricos
    para reutilização nos testes.
    """

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
    assert any(
        chart.chart_type == "histogram"
        for chart in charts
    )


def test_generate_automatic_charts_returns_empty_list_for_empty_dataframe():
    dataframe = pd.DataFrame()

    charts = generate_automatic_charts(dataframe)

    assert charts == []


def test_generate_automatic_charts_rejects_invalid_input():
    with pytest.raises(TypeError):
        generate_automatic_charts("invalid")


def test_generate_categorical_bar_chart_image_returns_png():
    dataframe = _create_mixed_dataframe()

    chart = generate_categorical_bar_chart_image(dataframe)

    assert isinstance(chart, StaticChartResult)
    assert chart.chart_type == "bar"
    assert chart.column_name == "Categoria"
    assert isinstance(chart.image_bytes, bytes)
    assert chart.image_bytes.startswith(b"\x89PNG\r\n\x1a\n")
    assert len(chart.image_bytes) > 0


def test_generate_numeric_histogram_image_returns_png():
    dataframe = _create_mixed_dataframe()

    chart = generate_numeric_histogram_image(dataframe)

    assert isinstance(chart, StaticChartResult)
    assert chart.chart_type == "histogram"
    assert chart.column_name == "Valor"
    assert isinstance(chart.image_bytes, bytes)
    assert chart.image_bytes.startswith(b"\x89PNG\r\n\x1a\n")
    assert len(chart.image_bytes) > 0


def test_generate_automatic_chart_images_returns_available_images():
    dataframe = _create_mixed_dataframe()

    charts = generate_automatic_chart_images(dataframe)

    assert len(charts) == 2
    assert all(
        isinstance(chart, StaticChartResult)
        for chart in charts
    )
    assert any(chart.chart_type == "bar" for chart in charts)
    assert any(
        chart.chart_type == "histogram"
        for chart in charts
    )
    assert all(
        chart.image_bytes.startswith(b"\x89PNG\r\n\x1a\n")
        for chart in charts
    )


def test_generate_automatic_chart_images_returns_empty_list_for_empty_dataframe():
    dataframe = pd.DataFrame()

    charts = generate_automatic_chart_images(dataframe)

    assert charts == []


def test_generate_automatic_chart_images_rejects_invalid_input():
    with pytest.raises(TypeError):
        generate_automatic_chart_images("invalid")