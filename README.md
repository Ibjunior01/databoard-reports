# DataBoard Reports

DataBoard Reports é uma plataforma web desenvolvida em Python com Flask para upload de planilhas CSV ou Excel, leitura inicial dos dados com Pandas, exibição de prévia dos dados e análise automática da estrutura da planilha.

O projeto está sendo desenvolvido em entregas pequenas e sequenciais, com foco em boas práticas de engenharia de software, testes automatizados, organização profissional de repositório e apresentação em portfólio no GitHub e LinkedIn.

## Objetivo do projeto

Criar uma aplicação web profissional onde empresas possam:

* enviar planilhas CSV ou Excel;
* visualizar uma prévia dos dados carregados;
* analisar automaticamente a estrutura dos dados;
* identificar colunas numéricas e categóricas;
* verificar valores ausentes por coluna;
* visualizar estatísticas numéricas básicas;
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

**Conversa 06 — Exibição da análise automática no dashboard**

Funcionalidades implementadas até agora:

* Base inicial Flask com application factory.

* Página inicial.

* Template base.

* CSS inicial com identidade visual dark/profissional.

* Configuração centralizada.

* Upload de arquivos CSV e Excel.

* Validação de extensões permitidas.

* Salvamento seguro dos arquivos enviados.

* Mensagens de sucesso e erro com flash.

* Leitura inicial de arquivos `.csv`, `.xlsx` e `.xls` com Pandas.

* Extração de metadados básicos da planilha:

  * nome do arquivo;
  * extensão;
  * quantidade de linhas;
  * quantidade de colunas;
  * nomes das colunas;
  * primeiras linhas da planilha.

* Exibição da prévia dos dados carregados no dashboard.

* Análise automática da planilha:

  * identificação de colunas numéricas;
  * identificação de colunas categóricas/texto;
  * contagem de valores ausentes por coluna;
  * percentual de valores ausentes por coluna;
  * estatísticas básicas das colunas numéricas.

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

Resultado atual esperado:

```text
23 passed
```

## Funcionalidades principais

### Upload de planilhas

A aplicação permite o envio de arquivos nos formatos:

```text
.csv
.xlsx
.xls
```

O upload possui validação de extensão, salvamento seguro do arquivo e tratamento de erros para arquivos inválidos ou não suportados.

### Leitura de dados com Pandas

O arquivo principal responsável pela leitura das planilhas é:

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

### Análise automática dos dados

O arquivo principal responsável pela análise automática é:

```text
app/services/analyzer.py
```

Ele possui funções para analisar um DataFrame e retornar informações como:

* total de linhas;
* total de colunas;
* colunas numéricas;
* colunas categóricas;
* valores ausentes;
* percentual de valores ausentes;
* estatísticas básicas das colunas numéricas.

### Dashboard

O arquivo principal da interface de dashboard é:

```text
app/templates/dashboard.html
```

Atualmente o dashboard exibe:

* dados básicos do arquivo enviado;
* lista de colunas identificadas;
* prévia tabular das primeiras linhas;
* resumo da análise automática;
* tipos de colunas;
* valores ausentes por coluna;
* estatísticas numéricas.

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

## Exemplo de análise automática

```python
{
    "numeric_columns": ["quantity", "revenue"],
    "categorical_columns": ["product", "category"],
    "missing_values": {
        "product": 0,
        "quantity": 0,
        "revenue": 0,
        "category": 2
    },
    "missing_percentage": {
        "product": 0.0,
        "quantity": 0.0,
        "revenue": 0.0,
        "category": 2.0
    },
    "numeric_statistics": {
        "quantity": {
            "mean": 10.5,
            "min": 1,
            "max": 50,
            "median": 8
        }
    }
}
```

## Testes automatizados

O projeto possui testes para:

* rotas principais da aplicação;
* upload de arquivos válidos;
* rejeição de arquivos inválidos;
* validação de extensões suportadas;
* leitura de arquivo CSV;
* leitura de arquivo Excel;
* geração de metadados;
* análise automática de DataFrame;
* identificação de colunas numéricas;
* identificação de colunas categóricas;
* cálculo de valores ausentes;
* cálculo de estatísticas numéricas;
* exibição da análise automática no dashboard.

## Resultado atual dos testes

```text
23 passed
```

## Próximas entregas planejadas

A próxima entrega provavelmente será:

**Conversa 07 — Gráficos automáticos com Plotly**

Escopo recomendado:

* criar função inicial em `app/services/charts.py`;
* gerar gráfico automático para colunas categóricas;
* gerar gráfico automático para colunas numéricas;
* integrar os gráficos ao dashboard;
* manter os gráficos simples e controlados;
* adicionar testes para a geração dos gráficos.

Fora do escopo da próxima entrega:

* banco de dados;
* histórico real de uploads;
* autenticação;
* exportação em PDF;
* deploy;
* CI/CD.
