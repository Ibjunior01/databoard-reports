"""
Inferência de esquema e classificação semântica de colunas.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import Any

import pandas as pd


DEFAULT_SAMPLE_SIZE = 5

IDENTIFIER_NAME_TOKENS = {
    "ID",
    "IDENTIFICADOR",
    "CODIGO",
    "MATRICULA",
    "CPF",
    "CNPJ",
    "CEP",
}

IDENTIFIER_SCORE_THRESHOLD = 0.60

PERCENTAGE_STRONG_NAME_TOKENS = {
    "PCT",
    "PERCENTUAL",
    "PERCENT",
    "PORCENTAGEM",
}

PERCENTAGE_CONTEXT_NAME_TOKENS = {
    "MARGEM",
    "TAXA",
    "DESCONTO",
}

PERCENTAGE_SCORE_THRESHOLD = 0.60


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


def calculate_identifier_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles an identifier.

    The score combines:
    - semantic signals from the normalized name;
    - uniqueness/cardinality;
    - dtype compatibility;
    - presence of usable values.

    The returned value is always between 0.0 and 1.0.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0

    name_tokens = set(profile.normalized_name.split("_"))

    if (
        profile.normalized_name == "ID"
        or profile.normalized_name.endswith("_ID")
        or profile.normalized_name.startswith("ID_")
    ):
        score += 0.65

    elif name_tokens & IDENTIFIER_NAME_TOKENS:
        score += 0.55

    if profile.unique_ratio >= 0.90:
        score += 0.20
    elif profile.unique_ratio >= 0.50:
        score += 0.10

    dtype = profile.pandas_dtype.lower()

    if "int" in dtype or "object" in dtype or "string" in dtype:
        score += 0.10

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_identifier_column(
    profile: ColumnProfile,
) -> bool:
    """
    Return whether the column has enough evidence to be an identifier.
    """
    return calculate_identifier_score(profile) >= IDENTIFIER_SCORE_THRESHOLD


def calculate_percentage_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a percentage.

    The score combines semantic signals from the column name
    with percentage patterns found in sampled values.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0

    name_tokens = set(profile.normalized_name.split("_"))

    if name_tokens & PERCENTAGE_STRONG_NAME_TOKENS:
        score += 0.65
    elif name_tokens & PERCENTAGE_CONTEXT_NAME_TOKENS:
        score += 0.30

    percentage_pattern = re.compile(r"^[+-]?\d+(?:[.,]\d+)?\s*%$")

    sample_values = [value for value in profile.sample_values if str(value).strip()]

    if sample_values:
        percentage_matches = sum(
            bool(percentage_pattern.match(str(value).strip()))
            for value in sample_values
        )

        percentage_ratio = percentage_matches / len(sample_values)

        if percentage_ratio >= 0.80:
            score += 0.60
        elif percentage_ratio >= 0.50:
            score += 0.45
        elif percentage_ratio > 0:
            score += 0.25

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_percentage_column(
    profile: ColumnProfile,
) -> bool:
    """
    Return whether the column has enough evidence to be a percentage.
    """
    return calculate_percentage_score(profile) >= PERCENTAGE_SCORE_THRESHOLD
