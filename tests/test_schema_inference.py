import pandas as pd
import pytest
from pathlib import Path

from app.services.schema_inference import (
    build_column_profiles,
    calculate_identifier_score,
    calculate_percentage_score,
    is_identifier_column,
    is_percentage_column,
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
