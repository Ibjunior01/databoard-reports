"""
Utilitários de data, hora e fuso horário do DataBoard Reports.
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import current_app, has_app_context

DEFAULT_TIMEZONE = "America/Fortaleza"


def get_configured_timezone_name() -> str:
    """
    Return the application timezone.

    Outside a Flask application context, the project default is used.
    """
    if has_app_context():
        return current_app.config.get(
            "APP_TIMEZONE",
            DEFAULT_TIMEZONE,
        )

    return DEFAULT_TIMEZONE


def get_timezone(
    timezone_name: str | None = None,
) -> ZoneInfo:
    """
    Return a validated IANA timezone.
    """
    selected_timezone = timezone_name or get_configured_timezone_name()

    try:
        return ZoneInfo(selected_timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Fuso horário inválido: {selected_timezone}") from exc


def to_local_datetime(
    value: datetime | None,
    timezone_name: str | None = None,
) -> datetime | None:
    """
    Convert a datetime to the configured local timezone.

    Naive datetime values are treated as UTC. This is important for
    SQLite, which may return timezone-aware database fields without
    tzinfo even when the values were originally persisted in UTC.
    """
    if value is None:
        return None

    normalized_value = value

    if normalized_value.tzinfo is None:
        normalized_value = normalized_value.replace(tzinfo=timezone.utc)

    return normalized_value.astimezone(get_timezone(timezone_name))


def format_local_datetime(
    value: datetime | None,
    format_string: str = "%d/%m/%Y %H:%M",
    timezone_name: str | None = None,
) -> str:
    """
    Format a datetime using the configured local timezone.
    """
    if value is None:
        return "Não informado"

    local_value = to_local_datetime(
        value,
        timezone_name=timezone_name,
    )

    return local_value.strftime(format_string)
