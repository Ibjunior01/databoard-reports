"""
Serviço de carregamento de dados.

Futuras responsabilidades:
- Ler arquivos CSV.
- Ler arquivos Excel.
- Validar estrutura dos arquivos.
- Retornar DataFrames do Pandas para análise.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
DEFAULT_PREVIEW_ROWS = 5


class UnsupportedFileTypeError(ValueError):
    """Raised when the uploaded file extension is not supported."""


@dataclass(frozen=True)
class SpreadsheetMetadata:
    """Basic metadata extracted from a spreadsheet file."""

    file_name: str
    file_extension: str
    rows: int
    columns: int
    column_names: list[str]
    preview: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def get_file_extension(file_path: str | Path) -> str:
    """Return the file extension in lowercase, including the dot."""
    return Path(file_path).suffix.lower()


def allowed_file(filename: str) -> bool:
    """Check if a filename has a supported spreadsheet extension."""
    if not filename:
        return False

    return get_file_extension(filename) in SUPPORTED_EXTENSIONS


def validate_file_path(file_path: str | Path) -> Path:
    """
    Validate whether the file exists and has a supported extension.

    Returns:
        Path: normalized Path object.

    Raises:
        FileNotFoundError: if the file does not exist.
        UnsupportedFileTypeError: if the file extension is not supported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    extension = get_file_extension(path)

    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Unsupported file extension: {extension}. "
            f"Supported extensions are: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    return path


def load_spreadsheet(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a Pandas DataFrame.

    Supported formats:
        - .csv
        - .xlsx
        - .xls
    """
    path = validate_file_path(file_path)
    extension = get_file_extension(path)

    if extension == ".csv":
        return pd.read_csv(path)

    if extension == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")

    if extension == ".xls":
        return pd.read_excel(path, engine="xlrd")

    raise UnsupportedFileTypeError(f"Unsupported file extension: {extension}")


def build_spreadsheet_metadata(
    dataframe: pd.DataFrame,
    file_path: str | Path,
    preview_rows: int = DEFAULT_PREVIEW_ROWS,
) -> SpreadsheetMetadata:
    """
    Build a structured metadata object from a Pandas DataFrame.
    """
    if preview_rows < 0:
        raise ValueError("preview_rows must be greater than or equal to zero.")

    path = Path(file_path)

    dataframe = dataframe.copy()
    dataframe.columns = [str(column) for column in dataframe.columns]

    preview_df = dataframe.head(preview_rows).copy().astype(object)
    preview_df = preview_df.where(pd.notna(preview_df), None)

    return SpreadsheetMetadata(
        file_name=path.name,
        file_extension=get_file_extension(path),
        rows=len(dataframe),
        columns=len(dataframe.columns),
        column_names=list(dataframe.columns),
        preview=preview_df.to_dict(orient="records"),
    )


def load_spreadsheet_metadata(
    file_path: str | Path,
    preview_rows: int = DEFAULT_PREVIEW_ROWS,
) -> dict[str, Any]:
    """
    Load a spreadsheet file and return basic metadata.

    Returns:
        dict: metadata containing row count, column count, column names,
        and a preview of the first rows.
    """
    dataframe = load_spreadsheet(file_path)
    metadata = build_spreadsheet_metadata(dataframe, file_path, preview_rows)

    return metadata.to_dict()


def read_spreadsheet(file_path: str | Path) -> pd.DataFrame:
    """
    Backward-compatible alias for load_spreadsheet.
    """
    return load_spreadsheet(file_path)


def get_spreadsheet_metadata(
    file_path: str | Path,
    preview_rows: int = DEFAULT_PREVIEW_ROWS,
) -> dict[str, Any]:
    """
    Backward-compatible alias for load_spreadsheet_metadata.
    """
    return load_spreadsheet_metadata(file_path, preview_rows)