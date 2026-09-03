"""
Serviço de análise automática de dados do DataBoard Reports.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from app.services.schema_inference import (
    SemanticClassification,
    SemanticType,
    classify_dataframe_schema,
)

METRIC_SEMANTIC_TYPES = {
    SemanticType.CURRENCY,
    SemanticType.PERCENTAGE,
    SemanticType.QUANTITY,
    SemanticType.NUMERIC,
}

CATEGORICAL_SEMANTIC_TYPES = {
    SemanticType.CATEGORY,
    SemanticType.BOOLEAN,
}


@dataclass(frozen=True)
class DataAnalysisResult:
    """
    Resultado estruturado da análise automática de um DataFrame.

    Os campos legados ``numeric_columns`` e ``categorical_columns`` são
    preservados para manter compatibilidade com dashboard e relatórios,
    mas passam a ser orientados pela classificação semântica.
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

    semantic_types: dict[str, str]
    semantic_confidence: dict[str, float]
    identifier_columns: list[str]
    datetime_columns: list[str]
    date_columns: list[str]
    percentage_columns: list[str]
    currency_columns: list[str]
    boolean_columns: list[str]
    quantity_columns: list[str]
    metric_columns: list[str]
    category_columns: list[str]
    text_columns: list[str]
    unknown_columns: list[str]

    def to_dict(self) -> dict[str, Any]:
        """
        Converte o resultado para um dicionário serializável.
        """
        return asdict(self)


def analyze_dataframe(
    dataframe: pd.DataFrame,
) -> DataAnalysisResult:
    """
    Analisa automaticamente um DataFrame utilizando inferência semântica.

    A análise não modifica o DataFrame recebido. Os nomes das colunas são
    convertidos para ``str`` apenas em uma cópia interna, garantindo
    consistência com os demais serviços da aplicação.

    Raises:
        TypeError: quando o argumento informado não é um DataFrame.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("O objeto informado deve ser um pandas.DataFrame.")

    analysis_dataframe = dataframe.copy()
    analysis_dataframe.columns = [str(column) for column in analysis_dataframe.columns]

    rows, columns = analysis_dataframe.shape
    column_names = list(analysis_dataframe.columns)

    classifications = classify_dataframe_schema(analysis_dataframe)

    semantic_types = {
        column: classification.semantic_type.value
        for column, classification in classifications.items()
    }

    semantic_confidence = {
        column: classification.confidence
        for column, classification in classifications.items()
    }

    identifier_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.IDENTIFIER},
    )
    datetime_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.DATETIME},
    )
    date_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.DATE},
    )
    percentage_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.PERCENTAGE},
    )
    currency_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.CURRENCY},
    )
    boolean_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.BOOLEAN},
    )
    quantity_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.QUANTITY},
    )
    category_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.CATEGORY},
    )
    text_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.TEXT},
    )
    unknown_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        {SemanticType.UNKNOWN},
    )

    metric_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        METRIC_SEMANTIC_TYPES,
    )

    # Mantidos por compatibilidade com dashboard e relatórios atuais.
    numeric_columns = list(metric_columns)
    categorical_columns = _columns_by_semantic_type(
        column_names,
        classifications,
        CATEGORICAL_SEMANTIC_TYPES,
    )

    missing_values_count = _calculate_missing_values_count(analysis_dataframe)
    missing_values_percent = _calculate_missing_values_percent(
        missing_values_count=missing_values_count,
        total_rows=rows,
    )
    unique_values_count = _calculate_unique_values_count(analysis_dataframe)
    numeric_statistics = _calculate_semantic_numeric_statistics(
        dataframe=analysis_dataframe,
        classifications=classifications,
        metric_columns=metric_columns,
    )

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
        semantic_types=semantic_types,
        semantic_confidence=semantic_confidence,
        identifier_columns=identifier_columns,
        datetime_columns=datetime_columns,
        date_columns=date_columns,
        percentage_columns=percentage_columns,
        currency_columns=currency_columns,
        boolean_columns=boolean_columns,
        quantity_columns=quantity_columns,
        metric_columns=metric_columns,
        category_columns=category_columns,
        text_columns=text_columns,
        unknown_columns=unknown_columns,
    )


def _columns_by_semantic_type(
    column_names: list[str],
    classifications: dict[str, SemanticClassification],
    semantic_types: set[SemanticType],
) -> list[str]:
    """
    Retorna colunas dos tipos solicitados preservando a ordem física.
    """
    return [
        column
        for column in column_names
        if (
            column in classifications
            and classifications[column].semantic_type in semantic_types
        )
    ]


def _calculate_missing_values_count(
    dataframe: pd.DataFrame,
) -> dict[str, int]:
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
        column: round(
            (missing_count / total_rows) * 100,
            2,
        )
        for column, missing_count in missing_values_count.items()
    }


def _calculate_unique_values_count(
    dataframe: pd.DataFrame,
) -> dict[str, int]:
    """
    Calcula valores únicos por coluna ignorando ausentes.
    """
    return {
        str(column): int(value)
        for column, value in dataframe.nunique(dropna=True).to_dict().items()
    }


def _calculate_semantic_numeric_statistics(
    dataframe: pd.DataFrame,
    classifications: dict[str, SemanticClassification],
    metric_columns: list[str],
) -> dict[str, dict[str, float | None]]:
    """
    Calcula estatísticas apenas para métricas semanticamente válidas.

    Identificadores, datas, booleanos e dimensões categóricas são
    deliberadamente excluídos. Métricas armazenadas como texto, como
    ``R$ 1.234,56`` ou ``15%``, são convertidas apenas em uma série
    temporária para análise; o DataFrame original permanece intacto.
    """
    statistics: dict[
        str,
        dict[str, float | None],
    ] = {}

    for column in metric_columns:
        classification = classifications[column]

        numeric_series = _coerce_metric_series(
            dataframe[column],
            classification.semantic_type,
        ).dropna()

        if numeric_series.empty:
            statistics[column] = {
                "mean": None,
                "min": None,
                "max": None,
                "median": None,
            }
            continue

        statistics[column] = {
            "mean": _to_float(numeric_series.mean()),
            "min": _to_float(numeric_series.min()),
            "max": _to_float(numeric_series.max()),
            "median": _to_float(numeric_series.median()),
        }

    return statistics


def _coerce_metric_series(
    series: pd.Series,
    semantic_type: SemanticType,
) -> pd.Series:
    """
    Converte uma métrica para números em uma cópia temporária.

    A conversão é aplicada somente depois que a inferência semântica
    classificou a coluna como métrica com confiança suficiente.
    """
    if pd.api.types.is_numeric_dtype(series.dtype):
        return pd.to_numeric(
            series,
            errors="coerce",
        )

    parsed_values = series.map(
        lambda value: _parse_metric_value(
            value,
            semantic_type,
        )
    )

    return pd.to_numeric(
        parsed_values,
        errors="coerce",
    )


def _parse_metric_value(
    value: Any,
    semantic_type: SemanticType,
) -> float | None:
    """
    Converte um valor textual de métrica sem alterar a fonte original.

    Suporta, de forma conservadora:
    - moeda brasileira, como ``R$ 6.925,94``;
    - percentuais, como ``13%``;
    - números com vírgula decimal;
    - números em formato decimal convencional.
    """
    if pd.isna(value):
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if not text:
        return None

    text = text.replace("\u00a0", "").replace(" ", "")

    if semantic_type is SemanticType.CURRENCY:
        text = re.sub(
            r"^(?:R\$|BRL)",
            "",
            text,
            flags=re.IGNORECASE,
        )

    if semantic_type is SemanticType.PERCENTAGE:
        text = text.removesuffix("%")

    if not text:
        return None

    # Formato com ponto e vírgula: decide pelo último separador.
    if "." in text and "," in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")

    elif "," in text:
        text = text.replace(",", ".")

    elif semantic_type is SemanticType.CURRENCY and re.fullmatch(
        r"[+-]?\d{1,3}(?:\.\d{3})+",
        text,
    ):
        text = text.replace(".", "")

    try:
        return float(text)
    except ValueError:
        return None


def _to_float(
    value: Any,
) -> float | None:
    """
    Converte valores Pandas/Numpy para ``float`` nativo.
    """
    if pd.isna(value):
        return None

    return float(value)
