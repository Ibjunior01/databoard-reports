"""
Inferência de esquema e classificação semântica de colunas.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
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

CURRENCY_STRONG_NAME_TOKENS = {
    "VALOR",
    "PRECO",
    "RECEITA",
    "FATURAMENTO",
    "CUSTO",
    "TOTAL",
}
CURRENCY_SCORE_THRESHOLD = 0.60

DATE_NAME_TOKENS = {
    "DATA",
    "DATE",
}
DATE_SCORE_THRESHOLD = 0.60
DATE_VALUE_PATTERN = re.compile(
    r"^(?:"
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|"
    r"\d{4}-\d{1,2}-\d{1,2}"
    r")"
    r"(?:[ T]\d{1,2}:\d{2}(?::\d{2})?)?$"
)

DATETIME_SCORE_THRESHOLD = 0.60

BOOLEAN_NAME_TOKENS = {
    "ATIVO",
    "ATIVA",
    "BOOL",
    "BOOLEAN",
    "BOOLEANO",
    "FLAG",
    "HABILITADO",
    "HABILITADA",
    "VALIDO",
    "VALIDA",
}
BOOLEAN_TEXT_VALUES = {
    "TRUE",
    "FALSE",
    "SIM",
    "NAO",
    "YES",
    "NO",
}
BOOLEAN_SCORE_THRESHOLD = 0.60

QUANTITY_NAME_TOKENS = {
    "QTD",
    "QTDE",
    "QUANTIDADE",
    "QTY",
    "QUANTITY",
}
QUANTITY_SCORE_THRESHOLD = 0.60

NUMERIC_SCORE_THRESHOLD = 0.60

CATEGORY_NAME_TOKENS = {
    "CATEGORIA",
    "CATEG",
    "TIPO",
    "STATUS",
    "SITUACAO",
    "REGIAO",
    "UNIDADE",
    "SERVICO",
    "PRODUTO",
    "VENDEDOR",
    "VENDEDORA",
    "SETOR",
    "DEPARTAMENTO",
    "GRUPO",
}
CATEGORY_SCORE_THRESHOLD = 0.60

TEXT_NAME_TOKENS = {
    "OBS",
    "OBSERVACAO",
    "OBSERVACOES",
    "DESCRICAO",
    "COMENTARIO",
    "COMENTARIOS",
    "MENSAGEM",
    "NOTA",
    "NOTAS",
    "TEXTO",
    "DETALHE",
    "DETALHES",
}
TEXT_SCORE_THRESHOLD = 0.60

NUMERIC_VALUE_PATTERN = re.compile(
    r"^[+-]?(?:"
    r"\d{1,3}(?:\.\d{3})+(?:,\d+)?"
    r"|"
    r"\d+(?:[.,]\d+)?"
    r")$"
)

CURRENCY_VALUE_PATTERN = re.compile(
    r"^(?:R\$\s*)?"
    r"[+-]?(?:"
    r"\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?"
    r"|"
    r"\d+(?:[.,]\d{1,2})?"
    r")$"
)

PERCENTAGE_VALUE_PATTERN = re.compile(r"^[+-]?\d+(?:[.,]\d+)?\s*%$")


class SemanticType(str, Enum):
    """Tipos semânticos suportados pela inferência de esquema."""

    IDENTIFIER = "identifier"
    DATETIME = "datetime"
    DATE = "date"
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    BOOLEAN = "boolean"
    QUANTITY = "quantity"
    NUMERIC = "numeric"
    CATEGORY = "category"
    TEXT = "text"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SemanticClassification:
    """Classificação semântica final de uma coluna."""

    column_name: str
    semantic_type: SemanticType
    confidence: float


@dataclass(frozen=True)
class ColumnProfile:
    """Perfil técnico extraído de uma coluna do DataFrame."""

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

    The profile contains structural evidence used by semantic inference
    without changing the original data.
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
    Build profiles for every DataFrame column preserving physical order.

    Position-based access avoids ambiguity when a DataFrame contains
    duplicated column labels.
    """
    profiles: list[ColumnProfile] = []

    for position in range(len(dataframe.columns)):
        series = dataframe.iloc[:, position]
        profiles.append(
            profile_column(
                series,
                sample_size=sample_size,
            )
        )

    return profiles


def _name_tokens(
    profile: ColumnProfile,
) -> set[str]:
    return {token for token in profile.normalized_name.split("_") if token}


def _sample_values(
    profile: ColumnProfile,
) -> list[Any]:
    return [
        value
        for value in profile.sample_values
        if pd.notna(value) and str(value).strip()
    ]


def _is_numeric_scalar(
    value: Any,
) -> bool:
    return (
        isinstance(
            value,
            (
                int,
                float,
            ),
        )
        and not isinstance(value, bool)
        and pd.notna(value)
    )


def _looks_like_numeric_value(
    value: Any,
) -> bool:
    if _is_numeric_scalar(value):
        return True

    if not isinstance(value, str):
        return False

    return bool(NUMERIC_VALUE_PATTERN.match(value.strip()))


def _numeric_sample_ratio(
    profile: ColumnProfile,
) -> float:
    values = _sample_values(profile)

    if not values:
        return 0.0

    matches = sum(_looks_like_numeric_value(value) for value in values)

    return matches / len(values)


def _sample_average_text_length(
    profile: ColumnProfile,
) -> float:
    values = _sample_values(profile)

    text_values = [str(value).strip() for value in values if isinstance(value, str)]

    if not text_values:
        return 0.0

    return sum(len(value) for value in text_values) / len(text_values)


def calculate_identifier_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles an identifier.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0
    name_tokens = _name_tokens(profile)

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
    return calculate_identifier_score(profile) >= IDENTIFIER_SCORE_THRESHOLD


def calculate_percentage_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a percentage.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0
    name_tokens = _name_tokens(profile)

    has_strong_name = bool(name_tokens & PERCENTAGE_STRONG_NAME_TOKENS)
    has_context_name = bool(name_tokens & PERCENTAGE_CONTEXT_NAME_TOKENS)

    if has_strong_name:
        score += 0.65
    elif has_context_name:
        score += 0.30

    values = _sample_values(profile)

    if values:
        percentage_matches = sum(
            bool(PERCENTAGE_VALUE_PATTERN.match(str(value).strip())) for value in values
        )

        percentage_ratio = percentage_matches / len(values)

        if percentage_ratio >= 0.80:
            score += 0.60
        elif percentage_ratio >= 0.50:
            score += 0.45
        elif percentage_ratio > 0:
            score += 0.25

        if has_context_name and percentage_ratio == 0:
            numeric_values = [
                float(value) for value in values if _is_numeric_scalar(value)
            ]

            if (
                len(numeric_values) == len(values)
                and numeric_values
                and all(0.0 <= value <= 1.0 for value in numeric_values)
            ):
                score += 0.35

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_percentage_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_percentage_score(profile) >= PERCENTAGE_SCORE_THRESHOLD


def calculate_currency_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a monetary value.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0
    name_tokens = _name_tokens(profile)
    has_currency_name = bool(name_tokens & CURRENCY_STRONG_NAME_TOKENS)

    if has_currency_name:
        score += 0.45

    values = _sample_values(profile)

    if values:
        explicit_currency_matches = sum(
            isinstance(value, str) and value.strip().upper().startswith("R$")
            for value in values
        )

        monetary_pattern_matches = sum(
            bool(CURRENCY_VALUE_PATTERN.match(str(value).strip())) for value in values
        )

        explicit_currency_ratio = explicit_currency_matches / len(values)

        monetary_pattern_ratio = monetary_pattern_matches / len(values)

        if explicit_currency_ratio >= 0.80:
            score += 0.60
        elif explicit_currency_ratio > 0:
            score += 0.40
        elif monetary_pattern_ratio >= 0.80 and has_currency_name:
            score += 0.30

    dtype = profile.pandas_dtype.lower()

    if ("float" in dtype or "int" in dtype) and has_currency_name:
        score += 0.20

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_currency_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_currency_score(profile) >= CURRENCY_SCORE_THRESHOLD


def _looks_like_date_value(
    value: Any,
) -> bool:
    """
    Return whether a sampled value resembles a date or datetime.

    Numeric values are deliberately not interpreted as dates.
    """
    if isinstance(
        value,
        (
            pd.Timestamp,
            datetime,
            date,
        ),
    ):
        return True

    if not isinstance(value, str):
        return False

    value = value.strip()

    if not value:
        return False

    return bool(DATE_VALUE_PATTERN.match(value))


def calculate_date_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a date.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0
    name_tokens = _name_tokens(profile)

    if name_tokens & DATE_NAME_TOKENS:
        score += 0.35

    dtype = profile.pandas_dtype.lower()

    if "datetime" in dtype:
        score += 0.60

    values = _sample_values(profile)

    if values:
        date_matches = sum(_looks_like_date_value(value) for value in values)

        date_ratio = date_matches / len(values)

        if date_ratio >= 0.80:
            score += 0.55
        elif date_ratio >= 0.50:
            score += 0.40
        elif date_ratio > 0:
            score += 0.20

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_date_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_date_score(profile) >= DATE_SCORE_THRESHOLD


def _looks_like_datetime_value(
    value: Any,
) -> bool:
    """
    Return whether a sampled value contains an actual time component.
    """
    if isinstance(
        value,
        (
            pd.Timestamp,
            datetime,
        ),
    ):
        return any(
            (
                value.hour,
                value.minute,
                value.second,
                value.microsecond,
            )
        )

    if not isinstance(value, str):
        return False

    value = value.strip()

    if not value:
        return False

    return bool(
        re.search(
            r"[ T]\d{1,2}:\d{2}(?::\d{2})?$",
            value,
        )
    )


def calculate_datetime_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a datetime.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0
    name_tokens = _name_tokens(profile)

    if "DATETIME" in name_tokens or "TIMESTAMP" in name_tokens:
        score += 0.50
    elif "DATA" in name_tokens and "HORA" in name_tokens:
        score += 0.50

    dtype = profile.pandas_dtype.lower()

    if "datetime" in dtype:
        score += 0.30

    values = _sample_values(profile)

    if values:
        datetime_matches = sum(_looks_like_datetime_value(value) for value in values)

        datetime_ratio = datetime_matches / len(values)

        if datetime_ratio >= 0.80:
            score += 0.65
        elif datetime_ratio >= 0.50:
            score += 0.45
        elif datetime_ratio > 0:
            score += 0.25

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_datetime_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_datetime_score(profile) >= DATETIME_SCORE_THRESHOLD


def calculate_boolean_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a boolean.

    Numeric 0/1 values alone are deliberately not enough.
    """
    if profile.non_null_count == 0:
        return 0.0

    score = 0.0
    name_tokens = _name_tokens(profile)

    has_boolean_name = bool(name_tokens & BOOLEAN_NAME_TOKENS)

    if has_boolean_name:
        score += 0.35

    dtype = profile.pandas_dtype.lower()

    if dtype in {
        "bool",
        "boolean",
    }:
        score += 0.70

    values = _sample_values(profile)

    if values:
        normalized_values = {normalize_column_name(value) for value in values}

        if normalized_values and normalized_values <= BOOLEAN_TEXT_VALUES:
            score += 0.65

        numeric_values = [value for value in values if _is_numeric_scalar(value)]

        if (
            has_boolean_name
            and len(numeric_values) == len(values)
            and numeric_values
            and {float(value) for value in numeric_values} <= {0.0, 1.0}
        ):
            score += 0.35

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_boolean_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_boolean_score(profile) >= BOOLEAN_SCORE_THRESHOLD


def calculate_quantity_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a quantity/count metric.

    Quantity inference intentionally requires semantic support from the
    column name so generic numeric columns are not mislabeled.
    """
    if profile.non_null_count == 0:
        return 0.0

    name_tokens = _name_tokens(profile)

    if not (name_tokens & QUANTITY_NAME_TOKENS):
        return 0.0

    score = 0.65
    dtype = profile.pandas_dtype.lower()

    if "int" in dtype or "float" in dtype:
        score += 0.20

    values = _sample_values(profile)

    if values:
        integer_like_matches = sum(
            (_is_numeric_scalar(value) and float(value).is_integer())
            or (isinstance(value, str) and value.strip().lstrip("+-").isdigit())
            for value in values
        )

        if integer_like_matches / len(values) >= 0.80:
            score += 0.10

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_quantity_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_quantity_score(profile) >= QUANTITY_SCORE_THRESHOLD


def calculate_numeric_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a generic numeric metric.
    """
    if profile.non_null_count == 0:
        return 0.0

    dtype = profile.pandas_dtype.lower()

    if dtype in {
        "bool",
        "boolean",
    }:
        return 0.0

    score = 0.0

    if "int" in dtype or "float" in dtype:
        score += 0.65
    else:
        numeric_ratio = _numeric_sample_ratio(profile)

        if numeric_ratio >= 0.80:
            score += 0.60
        elif numeric_ratio >= 0.50:
            score += 0.40

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_numeric_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_numeric_score(profile) >= NUMERIC_SCORE_THRESHOLD


def calculate_text_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles free-form text.
    """
    if profile.non_null_count == 0:
        return 0.0

    dtype = profile.pandas_dtype.lower()

    if not ("object" in dtype or "string" in dtype or "category" in dtype):
        return 0.0

    score = 0.0
    name_tokens = _name_tokens(profile)

    if name_tokens & TEXT_NAME_TOKENS:
        score += 0.65

    score += 0.15

    average_length = _sample_average_text_length(profile)

    if average_length >= 40:
        score += 0.40
    elif average_length >= 15:
        score += 0.30
    elif average_length >= 8:
        score += 0.20

    if profile.unique_ratio >= 0.50:
        score += 0.15

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_text_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_text_score(profile) >= TEXT_SCORE_THRESHOLD


def calculate_category_score(
    profile: ColumnProfile,
) -> float:
    """
    Calculate how strongly a column resembles a categorical dimension.
    """
    if profile.non_null_count == 0:
        return 0.0

    dtype = profile.pandas_dtype.lower()

    if not ("object" in dtype or "string" in dtype or "category" in dtype):
        return 0.0

    score = 0.20
    name_tokens = _name_tokens(profile)

    if name_tokens & CATEGORY_NAME_TOKENS:
        score += 0.50

    if profile.unique_ratio <= 0.20:
        score += 0.30

    if profile.unique_count <= 20:
        score += 0.10

    if profile.null_ratio <= 0.10:
        score += 0.05

    return min(score, 1.0)


def is_category_column(
    profile: ColumnProfile,
) -> bool:
    return calculate_category_score(profile) >= CATEGORY_SCORE_THRESHOLD


def classify_column_semantics(
    profile: ColumnProfile,
) -> SemanticClassification:
    """
    Classify one column using semantic detectors.

    Precedence is intentional. Types that protect against analytically
    dangerous misclassification, especially identifiers, are evaluated
    before generic numeric/category/text fallbacks.
    """
    candidates = [
        (
            SemanticType.IDENTIFIER,
            calculate_identifier_score(profile),
            IDENTIFIER_SCORE_THRESHOLD,
        ),
        (
            SemanticType.DATETIME,
            calculate_datetime_score(profile),
            DATETIME_SCORE_THRESHOLD,
        ),
        (
            SemanticType.DATE,
            calculate_date_score(profile),
            DATE_SCORE_THRESHOLD,
        ),
        (
            SemanticType.PERCENTAGE,
            calculate_percentage_score(profile),
            PERCENTAGE_SCORE_THRESHOLD,
        ),
        (
            SemanticType.CURRENCY,
            calculate_currency_score(profile),
            CURRENCY_SCORE_THRESHOLD,
        ),
        (
            SemanticType.BOOLEAN,
            calculate_boolean_score(profile),
            BOOLEAN_SCORE_THRESHOLD,
        ),
        (
            SemanticType.QUANTITY,
            calculate_quantity_score(profile),
            QUANTITY_SCORE_THRESHOLD,
        ),
        (
            SemanticType.NUMERIC,
            calculate_numeric_score(profile),
            NUMERIC_SCORE_THRESHOLD,
        ),
        (
            SemanticType.TEXT,
            calculate_text_score(profile),
            TEXT_SCORE_THRESHOLD,
        ),
        (
            SemanticType.CATEGORY,
            calculate_category_score(profile),
            CATEGORY_SCORE_THRESHOLD,
        ),
    ]

    for (
        semantic_type,
        score,
        threshold,
    ) in candidates:
        if score >= threshold:
            return SemanticClassification(
                column_name=profile.original_name,
                semantic_type=semantic_type,
                confidence=round(score, 4),
            )

    return SemanticClassification(
        column_name=profile.original_name,
        semantic_type=SemanticType.UNKNOWN,
        confidence=0.0,
    )


def classify_dataframe_schema(
    dataframe: pd.DataFrame,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> dict[str, SemanticClassification]:
    """
    Classify every column of a DataFrame preserving column order.

    Column position does not participate in semantic inference.
    """
    classifications: dict[
        str,
        SemanticClassification,
    ] = {}

    for profile in build_column_profiles(
        dataframe,
        sample_size=sample_size,
    ):
        classifications[profile.original_name] = classify_column_semantics(profile)

    return classifications
