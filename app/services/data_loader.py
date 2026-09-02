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
from zipfile import BadZipFile

import pandas as pd
from openpyxl.utils.exceptions import InvalidFileException
from xlrd.biffh import XLRDError


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
DEFAULT_PREVIEW_ROWS = 5
HEADER_SCAN_ROWS = 15
MIN_HEADER_NON_EMPTY_CELLS = 2


class UnsupportedFileTypeError(ValueError):
    """Raised when the uploaded file extension is not supported."""


class InvalidSpreadsheetError(ValueError):
    """Raised when a spreadsheet cannot be safely parsed."""


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


def detect_header_row(
    dataframe: pd.DataFrame,
) -> int:
    """
    Detect the most likely header row in a raw spreadsheet preview.

    The function expects a DataFrame loaded with header=None and returns
    the zero-based row index that most likely contains the table header.

    The scoring favors rows that:
    - contain multiple populated cells;
    - contain mostly textual labels;
    - contain unique labels;
    - are followed by rows with a compatible table width;
    - differ structurally from the following data row;
    - appear earlier in the file when candidates are otherwise similar.

    If no stronger candidate is found, row zero is returned.
    """
    if dataframe.empty:
        return 0

    best_row = 0
    best_score = float("-inf")

    rows_to_scan = min(
        len(dataframe),
        HEADER_SCAN_ROWS,
    )

    for row_index in range(rows_to_scan):
        row = dataframe.iloc[row_index]

        non_empty_values = [
            value for value in row.tolist() if pd.notna(value) and str(value).strip()
        ]

        non_empty_count = len(non_empty_values)

        if non_empty_count < MIN_HEADER_NON_EMPTY_CELLS:
            continue

        textual_count = sum(isinstance(value, str) for value in non_empty_values)

        text_ratio = textual_count / non_empty_count

        unique_count = len({str(value).strip().lower() for value in non_empty_values})

        uniqueness_ratio = unique_count / non_empty_count

        next_non_empty_count = 0
        next_text_ratio = 0.0

        if row_index + 1 < len(dataframe):
            next_row = dataframe.iloc[row_index + 1]

            next_values = [
                value
                for value in next_row.tolist()
                if pd.notna(value) and str(value).strip()
            ]

            next_non_empty_count = len(next_values)

            if next_non_empty_count:
                next_textual_count = sum(
                    isinstance(value, str) for value in next_values
                )

                next_text_ratio = next_textual_count / next_non_empty_count

        following_width_ratio = min(
            next_non_empty_count / non_empty_count,
            1.0,
        )

        text_contrast = max(
            text_ratio - next_text_ratio,
            0.0,
        )

        position_penalty = row_index * 0.1

        score = (
            non_empty_count
            + text_ratio * 6
            + uniqueness_ratio * 2
            + following_width_ratio * 2
            + text_contrast * 4
            - position_penalty
        )

        if score > best_score:
            best_score = score
            best_row = row_index

    return best_row


def load_spreadsheet(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a Pandas DataFrame.

    Supported formats:
        - .csv
        - .xlsx
        - .xls

    Raises:
        FileNotFoundError: if the file does not exist.
        UnsupportedFileTypeError: if the extension is not supported.
        InvalidSpreadsheetError: if the file cannot be parsed safely.
    """
    path = validate_file_path(file_path)
    extension = get_file_extension(path)

    try:
        if extension == ".csv":
            return pd.read_csv(path)

        if extension == ".xlsx":
            return pd.read_excel(
                path,
                engine="openpyxl",
            )

        if extension == ".xls":
            return pd.read_excel(
                path,
                engine="xlrd",
            )

    except (
        pd.errors.ParserError,
        UnicodeDecodeError,
        BadZipFile,
        InvalidFileException,
        XLRDError,
        ValueError,
        OSError,
    ) as exc:
        raise InvalidSpreadsheetError(
            f"Unable to read spreadsheet: {path.name}"
        ) from exc

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
