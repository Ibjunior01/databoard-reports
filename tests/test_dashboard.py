from pathlib import Path

from app.services.history import create_upload_record


def create_dashboard_upload(app, filename, content):
    upload_folder = Path(app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = upload_folder / filename
    file_path.write_text(
        content,
        encoding="utf-8",
    )

    return create_upload_record(
        file_name=filename,
        file_extension=".csv",
        file_path=str(file_path),
        row_count=2,
        column_count=3,
    )


def test_dashboard_without_uploads_shows_empty_state(
    client,
):
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Nenhum dado dispon\xc3\xadvel" in response.data


def test_dashboard_opens_latest_upload(
    app,
    client,
):
    with app.app_context():
        create_dashboard_upload(
            app,
            "primeiro.csv",
            (
                "VENDEDOR,VALOR_TOTAL,DATA_VENDA\n"
                "Ana,100,2026-01-01\n"
                "Bruno,200,2026-01-02\n"
            ),
        )

        latest = create_dashboard_upload(
            app,
            "mais_recente.csv",
            (
                "VENDEDOR,VALOR_TOTAL,DATA_VENDA\n"
                "Carla,300,2026-02-01\n"
                "Diego,400,2026-02-02\n"
            ),
        )

        latest_id = latest.id

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"mais_recente.csv" in response.data
    assert str(latest_id).encode() in response.data


def test_dashboard_can_select_specific_upload(
    app,
    client,
):
    with app.app_context():
        selected = create_dashboard_upload(
            app,
            "selecionado.csv",
            (
                "VENDEDOR,VALOR_TOTAL,DATA_VENDA\n"
                "Ana,150,2026-03-01\n"
                "Bruno,250,2026-03-02\n"
            ),
        )

        create_dashboard_upload(
            app,
            "outro.csv",
            (
                "VENDEDOR,VALOR_TOTAL,DATA_VENDA\n"
                "Carla,350,2026-04-01\n"
                "Diego,450,2026-04-02\n"
            ),
        )

        selected_id = selected.id

    response = client.get(f"/dashboard?upload_id={selected_id}")

    assert response.status_code == 200
    assert b"selecionado.csv" in response.data


def test_dashboard_invalid_upload_redirects(
    app,
    client,
):
    with app.app_context():
        create_dashboard_upload(
            app,
            "existente.csv",
            (
                "VENDEDOR,VALOR_TOTAL,DATA_VENDA\n"
                "Ana,100,2026-01-01\n"
                "Bruno,200,2026-01-02\n"
            ),
        )

    response = client.get(
        "/dashboard?upload_id=999999",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/dashboard")
