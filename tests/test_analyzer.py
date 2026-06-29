import pandas as pd
import pytest

from app.services.analyzer import DataAnalysisResult, analyze_dataframe


def test_analyze_dataframe_returns_analysis_result():
    dataframe = pd.DataFrame(
        {
            "Produto": ["Notebook", "Mouse", "Teclado"],
            "Quantidade": [10, 20, 30],
        }
    )

    result = analyze_dataframe(dataframe)

    assert isinstance(result, DataAnalysisResult)


def test_analyze_dataframe_returns_basic_shape_information():
    dataframe = pd.DataFrame(
        {
            "Produto": ["Notebook", "Mouse", "Teclado"],
            "Quantidade": [10, 20, 30],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.rows == 3
    assert result.columns == 2
    assert result.column_names == ["Produto", "Quantidade"]


def test_analyze_dataframe_detects_numeric_and_categorical_columns():
    dataframe = pd.DataFrame(
        {
            "Produto": ["Notebook", "Mouse", "Teclado"],
            "Categoria": ["Eletrônicos", "Acessórios", "Acessórios"],
            "Quantidade": [10, 20, 30],
            "Valor": [3500.0, 80.0, 150.0],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.numeric_columns == ["Quantidade", "Valor"]
    assert result.categorical_columns == ["Produto", "Categoria"]


def test_analyze_dataframe_calculates_missing_values_count():
    dataframe = pd.DataFrame(
        {
            "Produto": ["Notebook", None, "Teclado", "Monitor"],
            "Quantidade": [10, 20, None, 40],
            "Valor": [3500.0, None, 150.0, 900.0],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.missing_values_count == {
        "Produto": 1,
        "Quantidade": 1,
        "Valor": 1,
    }


def test_analyze_dataframe_calculates_missing_values_percent():
    dataframe = pd.DataFrame(
        {
            "Produto": ["Notebook", None, "Teclado", "Monitor"],
            "Quantidade": [10, 20, None, 40],
            "Valor": [3500.0, None, 150.0, 900.0],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.missing_values_percent == {
        "Produto": 25.0,
        "Quantidade": 25.0,
        "Valor": 25.0,
    }


def test_analyze_dataframe_calculates_unique_values_count():
    dataframe = pd.DataFrame(
        {
            "Produto": ["Notebook", "Mouse", "Mouse", None],
            "Categoria": ["Eletrônicos", "Acessórios", "Acessórios", "Monitores"],
            "Quantidade": [10, 20, 20, None],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.unique_values_count == {
        "Produto": 2,
        "Categoria": 3,
        "Quantidade": 2,
    }


def test_analyze_dataframe_calculates_numeric_statistics():
    dataframe = pd.DataFrame(
        {
            "Produto": ["Notebook", "Mouse", "Teclado", "Monitor"],
            "Quantidade": [10, 20, None, 40],
            "Valor": [100.0, 150.0, 200.0, None],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.numeric_statistics["Quantidade"]["mean"] == pytest.approx(23.333333)
    assert result.numeric_statistics["Quantidade"]["min"] == 10.0
    assert result.numeric_statistics["Quantidade"]["max"] == 40.0
    assert result.numeric_statistics["Quantidade"]["median"] == 20.0

    assert result.numeric_statistics["Valor"]["mean"] == 150.0
    assert result.numeric_statistics["Valor"]["min"] == 100.0
    assert result.numeric_statistics["Valor"]["max"] == 200.0
    assert result.numeric_statistics["Valor"]["median"] == 150.0


def test_analyze_dataframe_handles_empty_dataframe():
    dataframe = pd.DataFrame(
        columns=["Produto", "Quantidade", "Valor"]
    )

    result = analyze_dataframe(dataframe)

    assert result.rows == 0
    assert result.columns == 3
    assert result.column_names == ["Produto", "Quantidade", "Valor"]
    assert result.missing_values_count == {
        "Produto": 0,
        "Quantidade": 0,
        "Valor": 0,
    }
    assert result.missing_values_percent == {
        "Produto": 0.0,
        "Quantidade": 0.0,
        "Valor": 0.0,
    }
    assert result.unique_values_count == {
        "Produto": 0,
        "Quantidade": 0,
        "Valor": 0,
    }


def test_analyze_dataframe_rejects_non_dataframe_input():
    with pytest.raises(TypeError, match="pandas.DataFrame"):
        analyze_dataframe({"Produto": ["Notebook"]})