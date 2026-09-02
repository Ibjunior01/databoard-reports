from io import BytesIO


def test_upload_displays_automatic_charts(client):
    data = {
        "file": (
            BytesIO(b"Categoria,Valor\nA,10\nB,20\nA,30\nC,40\n"),
            "dados.csv",
        )
    }

    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Gráficos automáticos".encode("utf-8") in response.data
    assert b"plotly" in response.data.lower()


def test_uploads_with_same_name_use_different_physical_files(
    client,
    app,
):
    first_response = client.post(
        "/upload",
        data={
            "file": (
                BytesIO(b"Categoria,Valor\nA,10\nB,20\n"),
                "dados.csv",
            )
        },
        content_type="multipart/form-data",
    )

    second_response = client.post(
        "/upload",
        data={
            "file": (
                BytesIO(b"Categoria,Valor\nC,30\nD,40\n"),
                "dados.csv",
            )
        },
        content_type="multipart/form-data",
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    upload_folder = app.config["UPLOAD_FOLDER"]

    uploaded_files = list(
        upload_folder.glob("*_dados.csv")
    )

    assert len(uploaded_files) == 2
    assert uploaded_files[0].name != uploaded_files[1].name

    assert uploaded_files[0].read_bytes() != (
        uploaded_files[1].read_bytes()
    )


def test_invalid_excel_upload_is_removed_after_processing_failure(
    client,
    app,
):
    response = client.post(
        "/upload",
        data={
            "file": (
                BytesIO(b"isto nao e um arquivo excel valido"),
                "arquivo_invalido.xlsx",
            )
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200

    expected_message = (
        "Não foi possível processar o arquivo enviado. "
        "Verifique se ele é uma planilha válida e tente novamente."
    )

    assert expected_message.encode("utf-8") in response.data

    upload_folder = app.config["UPLOAD_FOLDER"]

    invalid_files = list(
        upload_folder.glob("*arquivo_invalido.xlsx")
    )

    assert invalid_files == []