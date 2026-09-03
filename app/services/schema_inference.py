"""
Inferência de esquema e classificação semântica de colunas.
"""

import re
import unicodedata
from typing import Any


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
