"""
Serviço de análise de dados.

Futuras responsabilidades:
- Identificar colunas numéricas e categóricas.
- Gerar indicadores automáticos.
- Calcular totais, médias, rankings e séries temporais.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class DataAnalysisResult:
    """
    Estrutura de resultado da análise automática de um DataFrame.

    Esta estrutura mantém a camada de análise desacoplada da interface web,
    facilitando testes, reutilização e futura integração com dashboards.
    """

    rows: int
    columns: int
    column_names: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]
    missing_values_count: dict[str, int]
    missing_values_percent: dict[str, float]
    unique_values_count: dict[str, int]
    numeric_statistics: dict[str, dict[str, float | None]]

    def to_dict(self) -> dict[str, Any]:
        """
        Converte o resultado da análise para dicionário.

        Isso será útil em etapas futuras para renderização em templates,
        geração de JSON, APIs ou relatórios.
        """
        return asdict(self)


def analyze_dataframe(dataframe: pd.DataFrame) -> DataAnalysisResult:
    """
    Analisa automaticamente um DataFrame do Pandas.

    Args:
        dataframe: DataFrame carregado a partir de uma planilha CSV ou Excel.

    Returns:
        DataAnalysisResult: objeto estruturado com informações gerais,
        colunas detectadas, valores ausentes, valores únicos e estatísticas
        numéricas básicas.

    Raises:
        TypeError: quando o argumento informado não é um DataFrame.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("O objeto informado deve ser um pandas.DataFrame.")

    rows, columns = dataframe.shape
    column_names = [str(column) for column in dataframe.columns]

    numeric_dataframe = dataframe.select_dtypes(include="number")
    categorical_dataframe = dataframe.select_dtypes(include=["object", "category", "bool"])

    numeric_columns = [str(column) for column in numeric_dataframe.columns]
    categorical_columns = [str(column) for column in categorical_dataframe.columns]

    missing_values_count = _calculate_missing_values_count(dataframe)
    missing_values_percent = _calculate_missing_values_percent(
        missing_values_count=missing_values_count,
        total_rows=rows,
    )
    unique_values_count = _calculate_unique_values_count(dataframe)
    numeric_statistics = _calculate_numeric_statistics(numeric_dataframe)

    return DataAnalysisResult(
        rows=rows,
        columns=columns,
        column_names=column_names,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        missing_values_count=missing_values_count,
        missing_values_percent=missing_values_percent,
        unique_values_count=unique_values_count,
        numeric_statistics=numeric_statistics,
    )


def _calculate_missing_values_count(dataframe: pd.DataFrame) -> dict[str, int]:
    """
    Calcula a quantidade de valores ausentes por coluna.
    """
    return {
        str(column): int(value)
        for column, value in dataframe.isna().sum().to_dict().items()
    }


def _calculate_missing_values_percent(
    missing_values_count: dict[str, int],
    total_rows: int,
) -> dict[str, float]:
    """
    Calcula o percentual de valores ausentes por coluna.
    """
    if total_rows == 0:
        return {column: 0.0 for column in missing_values_count}

    return {
        column: round((missing_count / total_rows) * 100, 2)
        for column, missing_count in missing_values_count.items()
    }


def _calculate_unique_values_count(dataframe: pd.DataFrame) -> dict[str, int]:
    """
    Calcula a quantidade de valores únicos por coluna, ignorando valores ausentes.
    """
    return {
        str(column): int(value)
        for column, value in dataframe.nunique(dropna=True).to_dict().items()
    }


def _calculate_numeric_statistics(
    numeric_dataframe: pd.DataFrame,
) -> dict[str, dict[str, float | None]]:
    """
    Calcula estatísticas básicas para colunas numéricas.
    """
    statistics: dict[str, dict[str, float | None]] = {}

    for column in numeric_dataframe.columns:
        series = numeric_dataframe[column].dropna()

        if series.empty:
            statistics[str(column)] = {
                "mean": None,
                "min": None,
                "max": None,
                "median": None,
            }
            continue

        statistics[str(column)] = {
            "mean": _to_float(series.mean()),
            "min": _to_float(series.min()),
            "max": _to_float(series.max()),
            "median": _to_float(series.median()),
        }

    return statistics


def _to_float(value: Any) -> float | None:
    """
    Converte valores numéricos do Pandas/Numpy para float nativo do Python.
    """
    if pd.isna(value):
        return None

    return float(value)