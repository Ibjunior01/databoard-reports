# DataBoard Reports

DataBoard Reports é uma plataforma web desenvolvida em Python com Flask para upload de planilhas CSV ou Excel, leitura inicial dos dados com Pandas e futura geração de dashboards automáticos, gráficos interativos e relatórios em PDF.

O projeto está sendo desenvolvido em entregas pequenas e sequenciais, com foco em boas práticas de engenharia de software, testes automatizados, organização profissional de repositório e apresentação em portfólio no GitHub e LinkedIn.

## Objetivo do projeto

Criar uma aplicação web profissional onde empresas possam:

* enviar planilhas CSV ou Excel;
* visualizar uma prévia dos dados carregados;
* gerar dashboards automáticos;
* visualizar gráficos interativos;
* exportar relatórios em PDF;
* consultar histórico de uploads e relatórios gerados.

## Stack planejada

* Python
* Flask
* Pandas
* Plotly
* SQLite
* SQLAlchemy
* ReportLab
* HTML/CSS
* Bootstrap
* Docker
* Pytest
* Git/GitHub

## Status atual

Entrega atual:

**Conversa 3 — Leitura inicial de arquivos com Pandas**

Funcionalidades implementadas até agora:

* Base inicial Flask com application factory.
* Página inicial.
* Template base.
* CSS inicial.
* Configuração centralizada.
* Upload de arquivos CSV e Excel.
* Validação de extensões permitidas.
* Salvamento seguro dos arquivos enviados.
* Mensagens de sucesso e erro com flash.
* Leitura inicial de arquivos `.csv`, `.xlsx` e `.xls` com Pandas.
* Extração de metadados básicos da planilha:

  * quantidade de linhas;
  * quantidade de colunas;
  * nomes das colunas;
  * primeiras linhas.
* Testes automatizados com Pytest.

## Estrutura do projeto

```text
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
```

## Como executar localmente

Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

No Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
python run.py
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Como rodar os testes

Execute:

```bash
python -m pytest
```

Resultado esperado:

```text
Todos os testes devem passar.
```

## Funcionalidades da Conversa 3

Nesta entrega foi criada a camada inicial de leitura de planilhas usando Pandas.

O arquivo principal é:

```text
app/services/data_loader.py
```

Ele possui funções para:

* validar se o arquivo existe;
* validar se a extensão é suportada;
* ler arquivos `.csv`;
* ler arquivos `.xlsx`;
* ler arquivos `.xls`;
* retornar um DataFrame Pandas;
* gerar metadados básicos da planilha;
* retornar uma prévia das primeiras linhas.

Extensões suportadas nesta fase:

```text
.csv
.xlsx
.xls
```

## Exemplo de metadados retornados

```python
{
    "file_name": "sales.csv",
    "file_extension": ".csv",
    "rows": 100,
    "columns": 5,
    "column_names": ["product", "quantity", "revenue", "date", "category"],
    "preview": [
        {
            "product": "Notebook",
            "quantity": 2,
            "revenue": 7000.0,
            "date": "2026-01-01",
            "category": "Electronics"
        }
    ]
}
```

## Testes adicionados nesta entrega

Foram adicionados testes para:

* validação de extensões suportadas;
* rejeição de extensões não suportadas;
* leitura de arquivo CSV;
* leitura de arquivo Excel;
* geração de metadados a partir de CSV;
* geração de metadados a partir de Excel;
* erro para arquivo inexistente;
* erro para extensão não suportada;
* controle da quantidade de linhas exibidas na prévia.

## Próximas entregas planejadas

A próxima entrega provavelmente será:

**Conversa 4 — Exibir uma prévia dos dados carregados na interface web**

Escopo provável:

* integrar a leitura da planilha ao fluxo de upload;
* após upload válido, carregar metadados;
* exibir quantidade de linhas e colunas;
* exibir nomes das colunas;
* exibir uma tabela simples com as primeiras linhas;
* manter sem dashboard, sem gráficos e sem banco de dados.
