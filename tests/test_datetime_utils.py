from datetime import datetime, timezone

from app.datetime_utils import (
    format_local_datetime,
    get_timezone,
    to_local_datetime,
)


def test_to_local_datetime_converts_utc_to_fortaleza():
    value = datetime(
        2026,
        9,
        3,
        14,
        46,
        tzinfo=timezone.utc,
    )

    local_value = to_local_datetime(
        value,
        timezone_name="America/Fortaleza",
    )

    assert local_value.hour == 11
    assert local_value.minute == 46
    assert local_value.utcoffset().total_seconds() == -10800


def test_to_local_datetime_treats_naive_datetime_as_utc():
    value = datetime( #noqa: DTZ001
        2026,
        9,
        3,
        14,
        46,
    )

    local_value = to_local_datetime(
        value,
        timezone_name="America/Fortaleza",
    )

    assert local_value.hour == 11
    assert local_value.minute == 46


def test_format_local_datetime_uses_pt_br_format():
    value = datetime(
        2026,
        9,
        3,
        14,
        46,
        3,
        tzinfo=timezone.utc,
    )

    formatted = format_local_datetime(
        value,
        format_string="%d/%m/%Y às %H:%M:%S",
        timezone_name="America/Fortaleza",
    )

    assert formatted == "03/09/2026 às 11:46:03"


def test_format_local_datetime_handles_none():
    assert format_local_datetime(None) == "Não informado"


def test_get_timezone_returns_valid_zone():
    timezone_value = get_timezone(
        "America/Fortaleza"
    )

    assert timezone_value.key == "America/Fortaleza"
