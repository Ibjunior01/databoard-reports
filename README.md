# DataBoard Reports

DataBoard Reports é uma aplicação web desenvolvida em Python e Flask para upload, processamento, análise e geração de relatórios de planilhas CSV e Excel.

O sistema utiliza Pandas para processamento dos dados, Plotly para visualizações, SQLite com SQLAlchemy para persistência e ReportLab para geração de relatórios PDF.

## Funcionalidades

Atualmente, a aplicação permite:

* enviar arquivos `.csv`, `.xlsx` e `.xls`;
* validar e armazenar os arquivos enviados;
* visualizar metadados e uma prévia dos dados;
* identificar colunas numéricas e categóricas;
* calcular valores ausentes e estatísticas numéricas;
* gerar gráficos automáticos com Plotly;
* registrar uploads no banco SQLite;
* consultar o histórico de uploads;
* reprocessar arquivos enviados anteriormente;
* gerar relatórios PDF com análise, estatísticas, gráficos e prévia dos dados;
* registrar os relatórios gerados no banco;
* listar e baixar novamente relatórios associados a um upload.

## Stack

* Python
* Flask
* Pandas
* Plotly
* Kaleido
* SQLite
* SQLAlchemy
* Flask-SQLAlchemy
* ReportLab
* HTML/CSS
* Bootstrap
* Pytest
* Docker
* Git/GitHub

## Arquitetura

O projeto segue uma estrutura modular baseada em serviços:

```text
app/
├── __init__.py
├── config.py
├── extensions.py
├── models.py
├── routes.py
│
├── services/
│   ├── analyzer.py
│   ├── charts.py
│   ├── data_loader.py
│   ├── history.py
│   ├── report_history.py
│   └── reports.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── history.html
│   ├── index.html
│   ├── upload.html
│   └── upload_detail.html
│
├── static/
│   └── css/
│       └── style.css
│
├── uploads/
└── reports/

tests/
├── test_analyzer.py
├── test_charts.py
├── test_data_loader.py
├── test_history.py
├── test_report_history.py
├── test_reports.py
├── test_routes.py
└── test_upload.py
```

## Fluxo principal

1. O usuário envia uma planilha.
2. O arquivo é validado e armazenado.
3. O Pandas carrega os dados.
4. A aplicação gera metadados, análise automática e gráficos.
5. O upload é registrado no banco de dados.
6. O usuário pode consultar ou reprocessar o upload.
7. Um relatório PDF pode ser gerado.
8. O relatório é armazenado fisicamente e registrado no banco.
9. Relatórios anteriores podem ser baixados novamente.

## Relatórios PDF

Os relatórios são gerados com ReportLab e podem incluir:

* informações do upload;
* resumo da análise automática;
* valores ausentes por coluna;
* estatísticas das colunas numéricas;
* prévia limitada da planilha;
* gráficos estáticos gerados com Plotly e Kaleido.

Os arquivos são armazenados em:

```text
app/reports/
```

Cada relatório também é relacionado ao seu upload de origem por meio do modelo `ReportRecord`.

## Rotas principais

| Método | Rota                      | Descrição                       |
| ------ | ------------------------- | ------------------------------- |
| GET    | `/`                       | Página inicial                  |
| GET    | `/upload`                 | Formulário de upload            |
| POST   | `/upload`                 | Processamento da planilha       |
| GET    | `/history`                | Histórico de uploads            |
| GET    | `/history/<id>`           | Detalhes do upload              |
| GET    | `/history/<id>/reprocess` | Reprocessamento do upload       |
| GET    | `/history/<id>/report`    | Geração de um novo PDF          |
| GET    | `/reports/<id>/download`  | Download de relatório existente |

## Banco de dados

A aplicação utiliza SQLite com Flask-SQLAlchemy.

Atualmente existem dois modelos principais:

* `UploadRecord`: armazena os dados do upload;
* `ReportRecord`: armazena os relatórios PDF gerados.

Um upload pode possuir vários relatórios.

## Executando o projeto

Clone o repositório:

```bash
git clone https://github.com/Ibjunior01/databoard-reports.git
cd databoard-reports
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Linux ou macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
python run.py
```

Acesse:

```text
http://127.0.0.1:5000
```

## Testes

Execute toda a suíte:

```bash
python -m pytest
```

Resultado atual:

```text
76 passed in 23.28s
```

Os testes utilizam SQLite em memória e pastas temporárias para uploads e relatórios.

## Arquivos locais

Os arquivos enviados são armazenados em:

```text
app/uploads/
```

Os relatórios são armazenados em:

```text
app/reports/
```

Esses arquivos não devem ser enviados ao GitHub.

## Status

**Entrega atual: Conversa 17 — Persistência dos relatórios gerados**

O histórico detalhado das entregas, arquivos modificados e próximos passos está disponível no arquivo:

```text
PROJECT_STATE.md
```

## Próxima etapa

A próxima evolução planejada é a criação de uma página geral de histórico de relatórios, permitindo consultar todos os PDFs gerados independentemente do upload de origem.

## Licença

Projeto desenvolvido para estudo, portfólio profissional e demonstração de conhecimentos em desenvolvimento web, análise de dados e engenharia de software.
