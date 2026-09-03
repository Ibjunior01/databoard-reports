from pathlib import Path

import pandas as pd
import pytest

from app.services.analyzer import (
    DataAnalysisResult,
    analyze_dataframe,
)


BENCHMARK_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "databoard_autodetect_benchmark.xlsx"
)


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
    assert result.column_names == [
        "Produto",
        "Quantidade",
    ]


def test_analyze_dataframe_detects_numeric_and_categorical_columns():
    dataframe = pd.DataFrame(
        {
            "Produto": [
                "Notebook",
                "Mouse",
                "Teclado",
            ],
            "Categoria": [
                "Eletrônicos",
                "Acessórios",
                "Acessórios",
            ],
            "Quantidade": [10, 20, 30],
            "Valor": [3500.0, 80.0, 150.0],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.numeric_columns == [
        "Quantidade",
        "Valor",
    ]
    assert result.categorical_columns == [
        "Produto",
        "Categoria",
    ]


def test_analyze_dataframe_calculates_missing_values_count():
    dataframe = pd.DataFrame(
        {
            "Produto": [
                "Notebook",
                None,
                "Teclado",
                "Monitor",
            ],
            "Quantidade": [10, 20, None, 40],
            "Valor": [
                3500.0,
                None,
                150.0,
                900.0,
            ],
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
            "Produto": [
                "Notebook",
                None,
                "Teclado",
                "Monitor",
            ],
            "Quantidade": [10, 20, None, 40],
            "Valor": [
                3500.0,
                None,
                150.0,
                900.0,
            ],
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
            "Produto": [
                "Notebook",
                "Mouse",
                "Mouse",
                None,
            ],
            "Categoria": [
                "Eletrônicos",
                "Acessórios",
                "Acessórios",
                "Monitores",
            ],
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
            "Produto": [
                "Notebook",
                "Mouse",
                "Teclado",
                "Monitor",
            ],
            "Quantidade": [10, 20, None, 40],
            "Valor": [
                100.0,
                150.0,
                200.0,
                None,
            ],
        }
    )

    result = analyze_dataframe(dataframe)

    assert (
        result.numeric_statistics["Quantidade"]["mean"]
        == pytest.approx(23.333333)
    )
    assert (
        result.numeric_statistics["Quantidade"]["min"]
        == 10.0
    )
    assert (
        result.numeric_statistics["Quantidade"]["max"]
        == 40.0
    )
    assert (
        result.numeric_statistics["Quantidade"]["median"]
        == 20.0
    )

    assert result.numeric_statistics["Valor"]["mean"] == 150.0
    assert result.numeric_statistics["Valor"]["min"] == 100.0
    assert result.numeric_statistics["Valor"]["max"] == 200.0
    assert result.numeric_statistics["Valor"]["median"] == 150.0


def test_analyze_dataframe_handles_empty_dataframe():
    dataframe = pd.DataFrame(
        columns=[
            "Produto",
            "Quantidade",
            "Valor",
        ]
    )

    result = analyze_dataframe(dataframe)

    assert result.rows == 0
    assert result.columns == 3
    assert result.column_names == [
        "Produto",
        "Quantidade",
        "Valor",
    ]

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
    with pytest.raises(
        TypeError,
        match="pandas.DataFrame",
    ):
        analyze_dataframe(
            {
                "Produto": ["Notebook"],
            }
        )


def test_analyzer_excludes_identifiers_from_numeric_columns():
    dataframe = pd.DataFrame(
        {
            "CLIENTE_ID": [
                1001,
                1002,
                1003,
            ],
            "QUANTIDADE": [
                2,
                4,
                6,
            ],
            "VALOR_TOTAL": [
                100.0,
                200.0,
                300.0,
            ],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.identifier_columns == [
        "CLIENTE_ID",
    ]

    assert result.numeric_columns == [
        "QUANTIDADE",
        "VALOR_TOTAL",
    ]

    assert "CLIENTE_ID" not in result.numeric_statistics


def test_analyzer_exposes_semantic_types_and_confidence():
    dataframe = pd.DataFrame(
        {
            "CLIENTE_ID": [1001, 1002, 1003],
            "DATA_VENDA": [
                "01/01/2026",
                "02/01/2026",
                "03/01/2026",
            ],
            "VALOR_TOTAL": [
                100.0,
                200.0,
                300.0,
            ],
            "ATIVO": [
                True,
                False,
                True,
            ],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.semantic_types == {
        "CLIENTE_ID": "identifier",
        "DATA_VENDA": "date",
        "VALOR_TOTAL": "currency",
        "ATIVO": "boolean",
    }

    assert all(
        0.0 <= confidence <= 1.0
        for confidence
        in result.semantic_confidence.values()
    )


def test_analyzer_parses_brazilian_currency_for_statistics():
    dataframe = pd.DataFrame(
        {
            "FATURAMENTO": [
                "R$ 1.250,00",
                "R$ 2.000,50",
                "R$ 749,50",
            ]
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.currency_columns == [
        "FATURAMENTO",
    ]
    assert result.numeric_columns == [
        "FATURAMENTO",
    ]

    statistics = result.numeric_statistics[
        "FATURAMENTO"
    ]

    assert statistics["mean"] == pytest.approx(
        1333.333333
    )
    assert statistics["min"] == 749.5
    assert statistics["max"] == 2000.5
    assert statistics["median"] == 1250.0


def test_analyzer_parses_percentage_strings_for_statistics():
    dataframe = pd.DataFrame(
        {
            "DESCONTO": [
                "10%",
                "15%",
                "20%",
            ]
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.percentage_columns == [
        "DESCONTO",
    ]

    statistics = result.numeric_statistics[
        "DESCONTO"
    ]

    assert statistics["mean"] == 15.0
    assert statistics["min"] == 10.0
    assert statistics["max"] == 20.0
    assert statistics["median"] == 15.0


def test_analyzer_separates_categories_text_and_booleans():
    dataframe = pd.DataFrame(
        {
            "REGIAO": [
                "Norte",
                "Sul",
                "Norte",
            ],
            "OBSERVACAO": [
                "Cliente solicitou atendimento prioritário.",
                "Contato realizado por telefone e registrado.",
                "Necessário revisar documentação do cadastro.",
            ],
            "ATIVO": [
                True,
                False,
                True,
            ],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result.category_columns == [
        "REGIAO",
    ]
    assert result.text_columns == [
        "OBSERVACAO",
    ]
    assert result.boolean_columns == [
        "ATIVO",
    ]

    assert result.categorical_columns == [
        "REGIAO",
        "ATIVO",
    ]


def test_analyzer_classifies_benchmark_base_semantically():
    dataframe = pd.read_excel(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    result = analyze_dataframe(dataframe)

    assert result.semantic_types == {
        "VENDEDOR": "category",
        "CLIENTE_ID": "identifier",
        "DATA_VENDA": "date",
        "REGIAO": "category",
        "VALOR_TOTAL": "currency",
        "PEDIDO_ID": "identifier",
        "QUANTIDADE": "quantity",
        "PRODUTO": "category",
        "MARGEM_PCT": "percentage",
        "ATIVO": "boolean",
    }

    assert result.identifier_columns == [
        "CLIENTE_ID",
        "PEDIDO_ID",
    ]

    assert result.metric_columns == [
        "VALOR_TOTAL",
        "QUANTIDADE",
        "MARGEM_PCT",
    ]


def test_analyzer_classification_is_independent_of_column_order():
    base_dataframe = pd.read_excel(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    reordered_dataframe = pd.read_excel(
        BENCHMARK_PATH,
        sheet_name="02_Colunas_Reordenadas",
    )

    base_result = analyze_dataframe(
        base_dataframe
    )
    reordered_result = analyze_dataframe(
        reordered_dataframe
    )

    assert base_result.semantic_types == (
        reordered_result.semantic_types
    )


def test_analyzer_classifies_challenging_benchmark_semantically():
    dataframe = pd.read_excel(
        BENCHMARK_PATH,
        sheet_name="03_Tipos_Desafiadores",
    )

    result = analyze_dataframe(dataframe)

    assert result.semantic_types == {
        "CODIGO_CLIENTE": "identifier",
        "DATA": "date",
        "FATURAMENTO": "currency",
        "DESCONTO": "percentage",
        "CATEGORIA": "category",
        "CEP": "identifier",
        "OBSERVACAO": "text",
    }

    assert result.numeric_columns == [
        "FATURAMENTO",
        "DESCONTO",
    ]

    assert result.categorical_columns == [
        "CATEGORIA",
    ]

    assert result.text_columns == [
        "OBSERVACAO",
    ]
