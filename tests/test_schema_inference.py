import pandas as pd
import pytest
from pathlib import Path

from app.services.schema_inference import (
    SemanticType,
    build_column_profiles,
    calculate_boolean_score,
    calculate_category_score,
    calculate_currency_score,
    calculate_date_score,
    calculate_datetime_score,
    calculate_identifier_score,
    calculate_numeric_score,
    calculate_percentage_score,
    calculate_quantity_score,
    calculate_text_score,
    classify_column_semantics,
    classify_dataframe_schema,
    is_boolean_column,
    is_category_column,
    is_currency_column,
    is_date_column,
    is_datetime_column,
    is_identifier_column,
    is_numeric_column,
    is_percentage_column,
    is_quantity_column,
    is_text_column,
    normalize_column_name,
    profile_column,
)

from app.services.data_loader import load_spreadsheet

BENCHMARK_PATH = (
    Path(__file__).parent / "fixtures" / "databoard_autodetect_benchmark.xlsx"
)


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


def test_profile_column_calculates_structural_metrics():
    series = pd.Series(
        [10, 20, 20, None],
        name="Valor Total",
    )

    profile = profile_column(series)

    assert profile.original_name == "Valor Total"
    assert profile.normalized_name == "VALOR_TOTAL"
    assert profile.total_count == 4
    assert profile.non_null_count == 3
    assert profile.null_count == 1
    assert profile.null_ratio == 0.25
    assert profile.unique_count == 2
    assert profile.unique_ratio == pytest.approx(2 / 3)
    assert profile.sample_values == [10.0, 20.0]


def test_profile_column_handles_all_null_values():
    series = pd.Series(
        [None, None, None],
        name="Campo Vazio",
    )

    profile = profile_column(series)

    assert profile.total_count == 3
    assert profile.non_null_count == 0
    assert profile.null_count == 3
    assert profile.null_ratio == 1.0
    assert profile.unique_count == 0
    assert profile.unique_ratio == 0.0
    assert profile.sample_values == []


def test_profile_column_limits_distinct_sample_values():
    series = pd.Series(
        ["A", "A", "B", "C", "D"],
        name="Categoria",
    )

    profile = profile_column(
        series,
        sample_size=2,
    )

    assert profile.sample_values == [
        "A",
        "B",
    ]


def test_build_column_profiles_preserves_dataframe_columns():
    dataframe = pd.DataFrame(
        {
            "Cliente ID": [101, 102],
            "Valor Total": [100.0, 200.0],
            "Região": ["Norte", "Sul"],
        }
    )

    profiles = build_column_profiles(dataframe)

    assert [profile.original_name for profile in profiles] == [
        "Cliente ID",
        "Valor Total",
        "Região",
    ]

    assert [profile.normalized_name for profile in profiles] == [
        "CLIENTE_ID",
        "VALOR_TOTAL",
        "REGIAO",
    ]


def test_cliente_id_is_detected_as_identifier():
    series = pd.Series(
        [1001, 1002, 1003, 1004],
        name="CLIENTE_ID",
    )

    profile = profile_column(series)

    assert is_identifier_column(profile)
    assert calculate_identifier_score(profile) >= 0.60


def test_pedido_id_is_detected_as_identifier():
    series = pd.Series(
        ["PED-001", "PED-002", "PED-003"],
        name="PEDIDO_ID",
    )

    profile = profile_column(series)

    assert is_identifier_column(profile)


def test_codigo_cliente_is_detected_as_identifier():
    series = pd.Series(
        [500001, 500002, 500003],
        name="CODIGO_CLIENTE",
    )

    profile = profile_column(series)

    assert is_identifier_column(profile)


def test_quantidade_is_not_detected_as_identifier():
    series = pd.Series(
        [1, 2, 3, 4],
        name="QUANTIDADE",
    )

    profile = profile_column(series)

    assert not is_identifier_column(profile)


def test_valor_total_is_not_detected_as_identifier():
    series = pd.Series(
        [100.50, 250.75, 399.90],
        name="VALOR_TOTAL",
    )

    profile = profile_column(series)

    assert not is_identifier_column(profile)


def test_benchmark_base_detects_expected_identifiers():
    dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    profiles = {
        profile.normalized_name: profile for profile in build_column_profiles(dataframe)
    }

    assert is_identifier_column(profiles["CLIENTE_ID"])

    assert is_identifier_column(profiles["PEDIDO_ID"])

    assert not is_identifier_column(profiles["QUANTIDADE"])

    assert not is_identifier_column(profiles["VALOR_TOTAL"])


def test_benchmark_challenging_types_detects_codigo_cliente():
    dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="03_Tipos_Desafiadores",
    )

    profiles = {
        profile.normalized_name: profile for profile in build_column_profiles(dataframe)
    }

    assert is_identifier_column(profiles["CODIGO_CLIENTE"])

    assert is_identifier_column(profiles["CEP"])

    assert not is_identifier_column(profiles["FATURAMENTO"])

    assert not is_identifier_column(profiles["DESCONTO"])


def test_margem_pct_is_detected_as_percentage():
    series = pd.Series(
        [10.5, 12.0, 8.7],
        name="MARGEM_PCT",
    )

    profile = profile_column(series)

    assert is_percentage_column(profile)
    assert calculate_percentage_score(profile) >= 0.60


def test_percentage_strings_are_detected():
    series = pd.Series(
        ["10%", "15%", "7,5%", "20%"],
        name="DESCONTO",
    )

    profile = profile_column(series)

    assert is_percentage_column(profile)


def test_valor_total_is_not_percentage():
    series = pd.Series(
        [100.50, 200.75, 350.00],
        name="VALOR_TOTAL",
    )

    profile = profile_column(series)

    assert not is_percentage_column(profile)


def test_faturamento_currency_strings_are_not_percentage():
    series = pd.Series(
        [
            "R$ 1.250,00",
            "R$ 980,50",
            "R$ 2.100,75",
        ],
        name="FATURAMENTO",
    )

    profile = profile_column(series)

    assert not is_percentage_column(profile)


def test_quantidade_is_not_percentage():
    series = pd.Series(
        [1, 2, 3, 4],
        name="QUANTIDADE",
    )

    profile = profile_column(series)

    assert not is_percentage_column(profile)


def test_benchmark_detects_percentage_columns():
    base_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    challenging_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="03_Tipos_Desafiadores",
    )

    base_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(base_dataframe)
    }

    challenging_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(challenging_dataframe)
    }

    assert is_percentage_column(base_profiles["MARGEM_PCT"])

    assert is_percentage_column(challenging_profiles["DESCONTO"])

    assert not is_percentage_column(base_profiles["VALOR_TOTAL"])

    assert not is_percentage_column(challenging_profiles["FATURAMENTO"])


def test_valor_total_is_detected_as_currency():
    series = pd.Series(
        [100.50, 250.75, 399.90],
        name="VALOR_TOTAL",
    )

    profile = profile_column(series)

    assert is_currency_column(profile)
    assert calculate_currency_score(profile) >= 0.60


def test_receita_is_detected_as_currency():
    series = pd.Series(
        [1000.0, 800.0, 1250.0],
        name="RECEITA",
    )

    profile = profile_column(series)

    assert is_currency_column(profile)


def test_currency_strings_are_detected():
    series = pd.Series(
        [
            "R$ 6.925,94",
            "R$ 1.250,00",
            "R$ 980,50",
        ],
        name="FATURAMENTO",
    )

    profile = profile_column(series)

    assert is_currency_column(profile)


def test_quantidade_is_not_currency():
    series = pd.Series(
        [1, 2, 3, 4],
        name="QUANTIDADE",
    )

    profile = profile_column(series)

    assert not is_currency_column(profile)


def test_cliente_id_is_not_currency():
    series = pd.Series(
        [1001, 1002, 1003],
        name="CLIENTE_ID",
    )

    profile = profile_column(series)

    assert not is_currency_column(profile)


def test_benchmark_detects_currency_columns():
    base_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    challenging_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="03_Tipos_Desafiadores",
    )

    header_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="04_Cabecalho_Linha3",
    )

    base_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(base_dataframe)
    }

    challenging_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(challenging_dataframe)
    }

    header_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(header_dataframe)
    }

    assert is_currency_column(base_profiles["VALOR_TOTAL"])

    assert is_currency_column(challenging_profiles["FATURAMENTO"])

    assert is_currency_column(header_profiles["RECEITA"])

    assert not is_currency_column(base_profiles["QUANTIDADE"])

    assert not is_currency_column(base_profiles["CLIENTE_ID"])


def test_datetime_dtype_is_detected_as_date():
    series = pd.Series(
        pd.to_datetime(
            [
                "2026-01-01",
                "2026-02-15",
                "2026-03-30",
            ]
        ),
        name="DATA_VENDA",
    )

    profile = profile_column(series)

    assert is_date_column(profile)
    assert calculate_date_score(profile) >= 0.60


def test_brazilian_date_strings_are_detected():
    series = pd.Series(
        [
            "01/01/2026",
            "15/02/2026",
            "30/03/2026",
        ],
        name="DATA",
    )

    profile = profile_column(series)

    assert is_date_column(profile)


def test_iso_date_strings_are_detected():
    series = pd.Series(
        [
            "2026-01-01",
            "2026-02-15",
            "2026-03-30",
        ],
        name="CRIADO_EM",
    )

    profile = profile_column(series)

    assert is_date_column(profile)


def test_numeric_identifier_is_not_detected_as_date():
    series = pd.Series(
        [500000, 500001, 500002],
        name="CODIGO_CLIENTE",
    )

    profile = profile_column(series)

    assert not is_date_column(profile)


def test_regular_text_is_not_detected_as_date():
    series = pd.Series(
        [
            "Premium",
            "Standard",
            "Basic",
        ],
        name="CATEGORIA",
    )

    profile = profile_column(series)

    assert not is_date_column(profile)


def test_benchmark_detects_date_columns():
    base_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    challenging_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="03_Tipos_Desafiadores",
    )

    header_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="04_Cabecalho_Linha3",
    )

    base_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(base_dataframe)
    }

    challenging_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(challenging_dataframe)
    }

    header_profiles = {
        profile.normalized_name: profile
        for profile in build_column_profiles(header_dataframe)
    }

    assert is_date_column(base_profiles["DATA_VENDA"])

    assert is_date_column(challenging_profiles["DATA"])

    assert is_date_column(header_profiles["DATA"])

    assert not is_date_column(challenging_profiles["CODIGO_CLIENTE"])

    assert not is_date_column(challenging_profiles["CEP"])


def test_datetime_values_are_detected():
    series = pd.Series(
        [
            "01/01/2026 14:35",
            "02/01/2026 09:10",
            "03/01/2026 18:45",
        ],
        name="DATA_HORA",
    )

    profile = profile_column(series)

    assert is_datetime_column(profile)
    assert calculate_datetime_score(profile) >= 0.60


def test_iso_datetime_values_are_detected():
    series = pd.Series(
        [
            "2026-01-01 14:35:00",
            "2026-01-02 09:10:00",
            "2026-01-03 18:45:00",
        ],
        name="CRIADO_EM",
    )

    profile = profile_column(series)

    assert is_datetime_column(profile)


def test_pandas_timestamp_with_time_is_detected_as_datetime():
    series = pd.Series(
        pd.to_datetime(
            [
                "2026-01-01 14:35",
                "2026-01-02 09:10",
                "2026-01-03 18:45",
            ]
        ),
        name="TIMESTAMP",
    )

    profile = profile_column(series)

    assert is_datetime_column(profile)


def test_plain_dates_are_not_detected_as_datetime():
    series = pd.Series(
        pd.to_datetime(
            [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03",
            ]
        ),
        name="DATA",
    )

    profile = profile_column(series)

    assert is_date_column(profile)
    assert not is_datetime_column(profile)


def test_numeric_identifier_is_not_datetime():
    series = pd.Series(
        [100001, 100002, 100003],
        name="PEDIDO_ID",
    )

    profile = profile_column(series)

    assert not is_datetime_column(profile)


def test_semantic_classifier_returns_identifier():
    profile = profile_column(
        pd.Series(
            [1001, 1002, 1003],
            name="CLIENTE_ID",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.IDENTIFIER
    assert result.confidence >= 0.60


def test_semantic_classifier_returns_datetime_before_date():
    profile = profile_column(
        pd.Series(
            [
                "01/01/2026 14:35",
                "02/01/2026 09:10",
                "03/01/2026 18:45",
            ],
            name="DATA_HORA",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.DATETIME


def test_semantic_classifier_returns_percentage():
    profile = profile_column(
        pd.Series(
            ["10%", "15%", "20%"],
            name="DESCONTO",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.PERCENTAGE


def test_semantic_classifier_returns_currency():
    profile = profile_column(
        pd.Series(
            [
                "R$ 1.250,00",
                "R$ 980,50",
                "R$ 2.100,75",
            ],
            name="FATURAMENTO",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.CURRENCY


def test_semantic_classifier_returns_unknown_without_evidence():
    profile = profile_column(
        pd.Series(
            [
                "texto qualquer",
                "outra informação",
                "conteúdo livre",
            ],
            name="CAMPO_X",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.UNKNOWN
    assert result.confidence == 0.0


def test_benchmark_unified_semantic_classification():
    base_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    challenging_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="03_Tipos_Desafiadores",
    )

    base_classifications = {
        profile.normalized_name: classify_column_semantics(profile)
        for profile in build_column_profiles(base_dataframe)
    }

    challenging_classifications = {
        profile.normalized_name: classify_column_semantics(profile)
        for profile in build_column_profiles(challenging_dataframe)
    }

    assert base_classifications["CLIENTE_ID"].semantic_type is SemanticType.IDENTIFIER

    assert base_classifications["PEDIDO_ID"].semantic_type is SemanticType.IDENTIFIER

    assert base_classifications["DATA_VENDA"].semantic_type is SemanticType.DATE

    assert base_classifications["MARGEM_PCT"].semantic_type is SemanticType.PERCENTAGE

    assert base_classifications["VALOR_TOTAL"].semantic_type is SemanticType.CURRENCY

    assert (
        challenging_classifications["CODIGO_CLIENTE"].semantic_type
        is SemanticType.IDENTIFIER
    )

    assert challenging_classifications["CEP"].semantic_type is SemanticType.IDENTIFIER

    assert challenging_classifications["DATA"].semantic_type is SemanticType.DATE

    assert (
        challenging_classifications["DESCONTO"].semantic_type is SemanticType.PERCENTAGE
    )

    assert (
        challenging_classifications["FATURAMENTO"].semantic_type
        is SemanticType.CURRENCY
    )


def test_native_boolean_is_detected():
    series = pd.Series(
        [True, False, True, False],
        name="ATIVO",
    )

    profile = profile_column(series)

    assert is_boolean_column(profile)
    assert calculate_boolean_score(profile) >= 0.60


def test_sim_nao_strings_are_detected_as_boolean():
    series = pd.Series(
        ["Sim", "Não", "Sim", "Não"],
        name="HABILITADO",
    )

    profile = profile_column(series)

    assert is_boolean_column(profile)


def test_zero_one_without_boolean_context_is_not_boolean():
    series = pd.Series(
        [0, 1, 0, 1],
        name="QUANTIDADE",
    )

    profile = profile_column(series)

    assert not is_boolean_column(profile)


def test_regular_status_is_not_boolean():
    series = pd.Series(
        [
            "Concluído",
            "Pendente",
            "Cancelado",
        ],
        name="STATUS",
    )

    profile = profile_column(series)

    assert not is_boolean_column(profile)


def test_semantic_classifier_returns_boolean():
    profile = profile_column(
        pd.Series(
            [True, False, True],
            name="ATIVO",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.BOOLEAN


def test_benchmark_detects_boolean_columns():
    dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    classifications = classify_dataframe_schema(dataframe)

    assert classifications["ATIVO"].semantic_type is SemanticType.BOOLEAN
    assert classifications["QUANTIDADE"].semantic_type is not SemanticType.BOOLEAN


def test_quantidade_is_detected_as_quantity():
    profile = profile_column(
        pd.Series(
            [1, 2, 3, 4],
            name="QUANTIDADE",
        )
    )

    assert is_quantity_column(profile)
    assert calculate_quantity_score(profile) >= 0.60


def test_qtd_is_detected_as_quantity():
    profile = profile_column(
        pd.Series(
            [2, 5, 10],
            name="QTD",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.QUANTITY


def test_generic_integer_is_not_quantity_without_name_evidence():
    profile = profile_column(
        pd.Series(
            [10, 20, 30],
            name="PONTUACAO",
        )
    )

    assert not is_quantity_column(profile)


def test_generic_numeric_metric_is_detected():
    profile = profile_column(
        pd.Series(
            [10.5, 20.0, 31.75],
            name="PONTUACAO",
        )
    )

    assert is_numeric_column(profile)
    assert calculate_numeric_score(profile) >= 0.60
    assert classify_column_semantics(profile).semantic_type is SemanticType.NUMERIC


def test_numeric_strings_can_be_detected_as_generic_numeric():
    profile = profile_column(
        pd.Series(
            ["10,5", "20,0", "31,75"],
            name="METRICA",
        )
    )

    assert is_numeric_column(profile)


def test_category_is_detected_from_low_cardinality_text():
    profile = profile_column(
        pd.Series(
            ["Norte", "Sul", "Norte", "Sul", "Centro"],
            name="REGIAO",
        )
    )

    assert is_category_column(profile)
    assert calculate_category_score(profile) >= 0.60
    assert classify_column_semantics(profile).semantic_type is SemanticType.CATEGORY


def test_free_text_is_detected_from_semantic_name():
    profile = profile_column(
        pd.Series(
            ["Revisar cadastro", "Cliente solicitou retorno", None],
            name="OBSERVACAO",
        )
    )

    assert is_text_column(profile)
    assert calculate_text_score(profile) >= 0.60
    assert classify_column_semantics(profile).semantic_type is SemanticType.TEXT


def test_mixed_ambiguous_values_remain_unknown():
    profile = profile_column(
        pd.Series(
            [1, "dois", "X", None],
            name="CAMPO_MISTO",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.UNKNOWN
    assert result.confidence == 0.0


def test_all_null_column_remains_unknown():
    profile = profile_column(
        pd.Series(
            [None, None, None],
            name="SEM_DADOS",
        )
    )

    result = classify_column_semantics(profile)

    assert result.semantic_type is SemanticType.UNKNOWN


def test_benchmark_full_semantic_schema():
    expected = {
        "01_Base_Realista": {
            "VENDEDOR": SemanticType.CATEGORY,
            "CLIENTE_ID": SemanticType.IDENTIFIER,
            "DATA_VENDA": SemanticType.DATE,
            "REGIAO": SemanticType.CATEGORY,
            "VALOR_TOTAL": SemanticType.CURRENCY,
            "PEDIDO_ID": SemanticType.IDENTIFIER,
            "QUANTIDADE": SemanticType.QUANTITY,
            "PRODUTO": SemanticType.CATEGORY,
            "MARGEM_PCT": SemanticType.PERCENTAGE,
            "ATIVO": SemanticType.BOOLEAN,
        },
        "03_Tipos_Desafiadores": {
            "CODIGO_CLIENTE": SemanticType.IDENTIFIER,
            "DATA": SemanticType.DATE,
            "FATURAMENTO": SemanticType.CURRENCY,
            "DESCONTO": SemanticType.PERCENTAGE,
            "CATEGORIA": SemanticType.CATEGORY,
            "CEP": SemanticType.IDENTIFIER,
            "OBSERVACAO": SemanticType.TEXT,
        },
        "04_Cabecalho_Linha3": {
            "DATA": SemanticType.DATE,
            "UNIDADE": SemanticType.CATEGORY,
            "SERVICO": SemanticType.CATEGORY,
            "QTD": SemanticType.QUANTITY,
            "RECEITA": SemanticType.CURRENCY,
            "STATUS": SemanticType.CATEGORY,
        },
    }

    for sheet_name, expected_types in expected.items():
        dataframe = load_spreadsheet(
            BENCHMARK_PATH,
            sheet_name=sheet_name,
        )

        classifications = classify_dataframe_schema(dataframe)

        assert {
            column_name: result.semantic_type
            for column_name, result in classifications.items()
        } == expected_types


def test_reordered_benchmark_has_equivalent_semantic_schema():
    base_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    reordered_dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="02_Colunas_Reordenadas",
    )

    base_schema = classify_dataframe_schema(base_dataframe)
    reordered_schema = classify_dataframe_schema(reordered_dataframe)

    assert set(base_schema) == set(reordered_schema)

    assert {
        column_name: result.semantic_type for column_name, result in base_schema.items()
    } == {
        column_name: result.semantic_type
        for column_name, result in reordered_schema.items()
    }


def test_dataframe_schema_preserves_column_order():
    dataframe = pd.DataFrame(
        {
            "CATEGORIA": ["A", "B"],
            "QUANTIDADE": [1, 2],
            "VALOR_TOTAL": [10.0, 20.0],
        }
    )

    classifications = classify_dataframe_schema(dataframe)

    assert list(classifications) == [
        "CATEGORIA",
        "QUANTIDADE",
        "VALOR_TOTAL",
    ]


def test_known_semantic_types_return_positive_confidence():
    dataframe = load_spreadsheet(
        BENCHMARK_PATH,
        sheet_name="01_Base_Realista",
    )

    classifications = classify_dataframe_schema(dataframe)

    assert all(
        classification.confidence >= 0.60 for classification in classifications.values()
    )
