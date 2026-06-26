# DataBoard Reports

DataBoard Reports é uma plataforma web desenvolvida em Python com Flask para permitir que empresas façam upload de planilhas CSV ou Excel, visualizem dashboards automáticos, gerem gráficos interativos e exportem relatórios em PDF.

O projeto está sendo desenvolvido em entregas pequenas e sequenciais, com foco em portfólio profissional para GitHub e divulgação no LinkedIn.

## Status do projeto

Entrega atual:

**Conversa 2 — Upload inicial de arquivos CSV e Excel**

Funcionalidades já implementadas:

- Estrutura inicial de aplicação Flask.
- Application factory.
- Página inicial.
- Template base.
- CSS inicial.
- Configuração centralizada.
- Dockerfile inicial.
- docker-compose.yml inicial.
- Testes iniciais com Pytest.
- Página de upload.
- Rota GET `/upload`.
- Rota POST `/upload`.
- Validação de extensões permitidas.
- Upload de arquivos `.csv`, `.xlsx` e `.xls`.
- Salvamento dos arquivos em `app/uploads/`.
- Mensagens de sucesso e erro com `flash`.

Ainda não implementado:

- Leitura dos dados com Pandas.
- Dashboard.
- Gráficos com Plotly.
- Banco de dados.
- Histórico de uploads.
- Exportação de PDF.
- Autenticação.

## Stack planejada

- Python
- Flask
- Pandas
- Plotly
- SQLite
- SQLAlchemy
- ReportLab
- HTML/CSS
- Bootstrap
- Docker
- Pytest
- Git/GitHub

## Estrutura do projeto

```txt
spreadsheet-dashboard-platform/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── analyzer.py
│   │   ├── charts.py
│   │   └── reports.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── dashboard.html
│   │   └── history.html
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── uploads/
│   │   └── .gitkeep
│   │
│   └── reports/
│       └── .gitkeep
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_data_loader.py
│   ├── test_routes.py
│   └── test_upload.py
│
├── sample_data/
│   └── .gitkeep
│
├── .env.example
├── .gitignore
├── conftest.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── PROJECT_STATE.md
└── run.py