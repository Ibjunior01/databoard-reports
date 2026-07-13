# DataBoard Reports

DataBoard Reports é uma plataforma web desenvolvida em Python com Flask para upload, processamento e análise de planilhas CSV ou Excel.

A aplicação utiliza Pandas para leitura e análise dos dados, Plotly para geração de gráficos interativos, SQLite com SQLAlchemy para persistência do histórico e ReportLab para exportação de relatórios em PDF.

O projeto está sendo construído em entregas pequenas e sequenciais, com foco em boas práticas de engenharia de software, testes automatizados, organização profissional de repositório e apresentação em portfólio no GitHub e LinkedIn.

## Objetivo do projeto

Criar uma aplicação web profissional que permita:

* enviar planilhas CSV ou Excel;
* visualizar uma prévia dos dados carregados;
* analisar automaticamente a estrutura dos dados;
* identificar colunas numéricas e categóricas;
* verificar valores ausentes por coluna;
* visualizar estatísticas numéricas básicas;
* gerar dashboards automáticos;
* visualizar gráficos interativos;
* registrar os uploads em banco de dados;
* consultar o histórico de arquivos enviados;
* visualizar os detalhes de cada upload;
* reprocessar arquivos enviados anteriormente;
* gerar e baixar relatórios em PDF;
* evoluir futuramente para dashboards customizáveis e relatórios avançados.

## Stack principal

* Python
* Flask
* Pandas
* Plotly
* SQLite
* SQLAlchemy
* Flask-SQLAlchemy
* ReportLab
* HTML
* CSS
* Bootstrap
* Docker
* Pytest
* Git
* GitHub

## Status atual

Entrega atual:

**Conversa 12 — Geração inicial de relatório PDF**

O sistema já possui um fluxo funcional para:

1. receber uma planilha;
2. validar sua extensão;
3. salvar o arquivo no servidor;
4. carregar os dados com Pandas;
5. extrair metadados;
6. gerar uma prévia dos dados;
7. realizar análise automática;
8. gerar gráficos interativos;
9. exibir o dashboard;
10. registrar o upload no banco SQLite;
11. listar uploads anteriores;
12. abrir os detalhes de um upload;
13. reprocessar um arquivo antigo;
14. gerar um relatório PDF;
15. baixar o relatório pelo navegador.

## Funcionalidades implementadas

### Estrutura Flask

* Application factory.
* Configuração centralizada.
* Uso de Blueprint para organização das rotas.
* Templates com herança Jinja.
* Arquivos estáticos organizados.
* Identidade visual dark e profissional.

### Upload de planilhas

A aplicação permite o envio de arquivos nos formatos:

```text
.csv
.xlsx
.xls
```

O fluxo de upload possui:

* validação de extensão;
* rejeição de arquivos inválidos;
* sanitização do nome com `secure_filename`;
* salvamento do arquivo no servidor;
* tratamento de erros;
* mensagens de sucesso e erro;
* registro do upload no banco de dados.

### Leitura de dados com Pandas

O serviço responsável pela leitura das planilhas está em:

```text
app/services/data_loader.py
```

Ele permite:

* validar se o arquivo existe;
* validar se a extensão é suportada;
* carregar arquivos CSV;
* carregar arquivos XLSX;
* carregar arquivos XLS;
* retornar um DataFrame Pandas;
* extrair metadados básicos;
* retornar uma prévia das primeiras linhas.

### Metadados da planilha

Após o processamento, o sistema extrai:

* nome do arquivo;
* extensão;
* quantidade de linhas;
* quantidade de colunas;
* nomes das colunas;
* primeiras linhas da planilha;
* caminho físico do arquivo salvo.

### Análise automática

O serviço responsável pela análise está em:

```text
app/services/analyzer.py
```

A análise automática identifica:

* total de linhas;
* total de colunas;
* colunas numéricas;
* colunas categóricas;
* valores ausentes por coluna;
* percentual de valores ausentes;
* média das colunas numéricas;
* mediana das colunas numéricas;
* menor valor;
* maior valor;
* estatísticas numéricas básicas.

### Dashboard

O dashboard está localizado em:

```text
app/templates/dashboard.html
```

Atualmente ele exibe:

* informações básicas do arquivo;
* nomes das colunas;
* prévia tabular dos dados;
* resumo da análise automática;
* colunas numéricas;
* colunas categóricas;
* qualidade dos dados;
* valores ausentes;
* estatísticas numéricas;
* gráficos automáticos com Plotly.

### Gráficos automáticos com Plotly

O serviço responsável pelos gráficos está em:

```text
app/services/charts.py
```

O sistema gera automaticamente:

* gráfico de barras para coluna categórica;
* histograma para coluna numérica;
* estado vazio quando não existem colunas compatíveis.

Os gráficos seguem a identidade visual dark do DataBoard Reports.

### Histórico de uploads

Cada upload válido gera um registro no banco SQLite.

O modelo principal está em:

```text
app/models.py
```

O histórico armazena:

* ID;
* nome do arquivo;
* extensão;
* quantidade de linhas;
* quantidade de colunas;
* caminho físico do arquivo;
* data e hora do upload.

A listagem pode ser acessada em:

```text
/history
```

### Detalhes do upload

Cada registro possui uma página individual:

```text
/history/<id>
```

A página apresenta:

* ID do upload;
* nome do arquivo;
* extensão;
* quantidade de linhas;
* quantidade de colunas;
* data e hora do upload;
* caminho salvo do arquivo;
* botão para reprocessamento;
* botão para geração de PDF.

Uploads inexistentes retornam erro HTTP 404.

### Reprocessamento de uploads antigos

A rota de reprocessamento permite reutilizar um arquivo salvo anteriormente:

```text
/history/<id>/reprocess
```

Durante o reprocessamento, o sistema:

* localiza o arquivo pelo campo `file_path`;
* verifica se o arquivo ainda existe;
* recarrega a planilha com Pandas;
* recalcula os metadados;
* recria a prévia;
* executa novamente a análise automática;
* gera novamente os gráficos;
* renderiza o dashboard atualizado.

Quando o arquivo físico não existe mais, uma mensagem amigável é exibida.

### Relatórios em PDF

O serviço responsável pela geração de relatórios está em:

```text
app/services/reports.py
```

A rota de geração é:

```text
/history/<id>/report
```

A primeira versão do relatório contém:

* título do sistema;
* descrição do relatório;
* ID do upload;
* nome do arquivo;
* extensão;
* quantidade de linhas;
* quantidade de colunas;
* data do upload;
* data e hora de geração.

Os relatórios:

* são gerados com ReportLab;
* possuem layout tabular;
* utilizam nome seguro e único;
* são armazenados em `app/reports/`;
* são enviados ao navegador para download;
* suportam quebra de linha em nomes de arquivos extensos;
* tratam caracteres especiais no nome do arquivo.

## Estrutura do projeto

```text
spreadsheet-dashboard-platform/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── analyzer.py
│   │   ├── charts.py
│   │   ├── history.py
│   │   └── reports.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   └── upload_detail.html
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
│   ├── test_charts.py
│   ├── test_data_loader.py
│   ├── test_history.py
│   ├── test_reports.py
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

## Banco de dados

O projeto utiliza SQLite com Flask-SQLAlchemy.

A configuração do banco está centralizada em:

```text
app/config.py
```

A instância do SQLAlchemy está em:

```text
app/extensions.py
```

As tabelas são inicializadas durante a criação da aplicação.

Durante os testes, o projeto utiliza um banco SQLite em memória para evitar alterações no banco local.

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Ibjunior01/databoard-reports.git
```

Entre na pasta:

```bash
cd databoard-reports
```

### 2. Criar o ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

No Prompt de Comando:

```cmd
venv\Scripts\activate
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação

```bash
python run.py
```

### 6. Acessar no navegador

```text
http://127.0.0.1:5000
```

## Rotas principais

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Página inicial |
| GET | `/upload` | Formulário de upload |
| POST | `/upload` | Processamento do arquivo |
| GET | `/history` | Histórico de uploads |
| GET | `/history/<id>` | Detalhes de um upload |
| GET | `/history/<id>/reprocess` | Reprocessamento de upload |
| GET | `/history/<id>/report` | Geração e download do PDF |

## Como executar os testes

Execute toda a suíte:

```bash
python -m pytest
```

Para uma saída mais detalhada:

```bash
python -m pytest -v
```

Para executar apenas os testes de relatórios:

```bash
python -m pytest tests/test_reports.py -v
```

Resultado atual:

```text
46 passed
```

## Testes automatizados

O projeto possui testes para:

* rotas principais;
* página inicial;
* tela de upload;
* upload de arquivos válidos;
* rejeição de arquivos inválidos;
* validação de extensões;
* leitura de arquivos CSV;
* leitura de arquivos Excel;
* extração de metadados;
* geração de prévia;
* análise automática;
* identificação de colunas numéricas;
* identificação de colunas categóricas;
* cálculo de valores ausentes;
* cálculo de percentuais de valores ausentes;
* cálculo de estatísticas numéricas;
* geração de gráficos;
* estado vazio dos gráficos;
* criação de registros no histórico;
* listagem do histórico;
* página de detalhes;
* erro 404 para registros inexistentes;
* persistência do caminho do arquivo;
* reprocessamento de uploads;
* arquivo físico inexistente;
* geração física do PDF;
* validação do cabeçalho `%PDF`;
* criação automática da pasta de relatórios;
* botão de geração do PDF;
* download do relatório;
* erro 404 ao gerar relatório de upload inexistente.

## Exemplo de metadados

```python
{
    "file_name": "sales.csv",
    "file_extension": ".csv",
    "rows": 100,
    "columns": 5,
    "column_names": [
        "product",
        "quantity",
        "revenue",
        "date",
        "category"
    ],
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
    "numeric_columns": [
        "quantity",
        "revenue"
    ],
    "categorical_columns": [
        "product",
        "category"
    ],
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

## Arquivos gerados localmente

Os arquivos enviados são armazenados em:

```text
app/uploads/
```

Os relatórios PDF são armazenados em:

```text
app/reports/
```

Arquivos gerados localmente não devem ser enviados para o GitHub.

O `.gitignore` deve conter:

```gitignore
app/uploads/*
!app/uploads/.gitkeep

app/reports/*.pdf
!app/reports/.gitkeep

instance/
*.sqlite3
```

## Próxima entrega planejada

### Conversa 13 — Inclusão da análise automática no relatório PDF

O objetivo da próxima entrega será evoluir o relatório básico para incluir um resumo da análise automática da planilha.

Escopo inicial recomendado:

* localizar o arquivo original pelo campo `file_path`;
* recarregar a planilha com o serviço de dados;
* reutilizar o analisador existente;
* incluir no PDF a quantidade de colunas numéricas;
* incluir a quantidade de colunas categóricas;
* incluir o total de valores ausentes;
* listar os nomes das colunas numéricas;
* listar os nomes das colunas categóricas;
* tratar arquivos físicos inexistentes;
* criar testes específicos para o relatório com análise.

Permanecem fora do próximo escopo:

* gráficos Plotly dentro do PDF;
* prévia completa da planilha no PDF;
* persistência dos relatórios no banco;
* histórico de relatórios;
* autenticação;
* permissões por usuário;
* dashboards customizáveis;
* upload múltiplo;
* CI/CD;
* deploy em produção.

## Roadmap futuro

* Relatórios PDF com análise automática.
* Inclusão de gráficos no PDF.
* Inclusão de prévia tabular no PDF.
* Persistência dos relatórios no banco.
* Histórico de relatórios gerados.
* Exclusão de registros do histórico.
* Upload múltiplo.
* Filtros avançados.
* Dashboards customizáveis.
* Autenticação.
* Controle de acesso por usuário.
* Migrações com Flask-Migrate.
* Dockerização completa.
* Pipeline CI/CD.
* Deploy em ambiente de produção.

## Licença

Este projeto está sendo desenvolvido para fins de estudo, portfólio profissional e demonstração de conhecimentos em desenvolvimento web, análise de dados e engenharia de software.