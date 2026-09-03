"""
Inferência de esquema e classificação semântica de colunas.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import Any

import pandas as pd


DEFAULT_SAMPLE_SIZE = 5


@dataclass(frozen=True)
class ColumnProfile:
    """
    Technical profile extracted from a DataFrame column.
    """

    original_name: str
    normalized_name: str
    pandas_dtype: str
    total_count: int
    non_null_count: int
    null_count: int
    null_ratio: float
    unique_count: int
    unique_ratio: float
    sample_values: list[Any]


def normalize_column_name(column_name: Any) -> str:
    """
    Normalize a column name for semantic analysis.

    Examples:
        "Valor Total" -> "VALOR_TOTAL"
        "Código Cliente" -> "CODIGO_CLIENTE"
        "margem_pct" -> "MARGEM_PCT"

    The original DataFrame column name is not modified by this function.
    """
    if column_name is None:
        return ""

    normalized = str(column_name).strip()

    if not normalized:
        return ""

    normalized = unicodedata.normalize(
        "NFKD",
        normalized,
    )

    normalized = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )

    normalized = normalized.upper()

    normalized = re.sub(
        r"[^A-Z0-9]+",
        "_",
        normalized,
    )

    normalized = re.sub(
        r"_+",
        "_",
        normalized,
    )

    return normalized.strip("_")


def profile_column(
    series: pd.Series,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> ColumnProfile:
    """
    Build a technical profile for a DataFrame column.

    The profile contains structural evidence that can later be used
    by semantic inference without changing the original data.
    """
    if sample_size < 0:
        raise ValueError("sample_size must be greater than or equal to zero.")

    total_count = len(series)
    null_count = int(series.isna().sum())
    non_null_count = total_count - null_count

    unique_count = int(
        series.nunique(
            dropna=True,
        )
    )

    null_ratio = null_count / total_count if total_count else 0.0

    unique_ratio = unique_count / non_null_count if non_null_count else 0.0

    sample_values = series.dropna().drop_duplicates().head(sample_size).tolist()

    return ColumnProfile(
        original_name=str(series.name),
        normalized_name=normalize_column_name(series.name),
        pandas_dtype=str(series.dtype),
        total_count=total_count,
        non_null_count=non_null_count,
        null_count=null_count,
        null_ratio=null_ratio,
        unique_count=unique_count,
        unique_ratio=unique_ratio,
        sample_values=sample_values,
    )


def build_column_profiles(
    dataframe: pd.DataFrame,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> list[ColumnProfile]:
    """
    Build profiles for every DataFrame column preserving column order.
    """
    return [
        profile_column(
            dataframe[column],
            sample_size=sample_size,
        )
        for column in dataframe.columns
    ]
