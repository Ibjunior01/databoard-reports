import pandas as pd
import pytest

from app.services.charts import (
    ChartResult,
    generate_automatic_charts,
    generate_categorical_bar_chart,
    generate_numeric_histogram,
)


def test_generate_categorical_bar_chart_returns_chart_result():
    dataframe = pd.DataFrame(
        {
            "Categoria": ["A", "B", "A", "C"],
            "Valor": [10, 20, 30, 40],
        }
    )

    chart = generate_categorical_bar_chart(dataframe)

    assert isinstance(chart, ChartResult)
    assert chart.chart_type == "bar"
    assert chart.column_name == "Categoria"
    assert "plotly" in chart.html.lower()


def test_generate_numeric_histogram_returns_chart_result():
    dataframe = pd.DataFrame(
        {
            "Categoria": ["A", "B", "A", "C"],
            "Valor": [10, 20, 30, 40],
        }
    )

    chart = generate_numeric_histogram(dataframe)

    assert isinstance(chart, ChartResult)
    assert chart.chart_type == "histogram"
    assert chart.column_name == "Valor"
    assert "plotly" in chart.html.lower()


def test_generate_automatic_charts_returns_available_charts():
    dataframe = pd.DataFrame(
        {
            "Categoria": ["A", "B", "A", "C"],
            "Valor": [10, 20, 30, 40],
        }
    )

    charts = generate_automatic_charts(dataframe)

    assert len(charts) == 2
    assert any(chart.chart_type == "bar" for chart in charts)
    assert any(chart.chart_type == "histogram" for chart in charts)


def test_generate_automatic_charts_returns_empty_list_for_empty_dataframe():
    dataframe = pd.DataFrame()

    charts = generate_automatic_charts(dataframe)

    assert charts == []


def test_generate_automatic_charts_rejects_invalid_input():
    with pytest.raises(TypeError):
        generate_automatic_charts("invalid")