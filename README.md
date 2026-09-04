# DataBoard Reports

[![CI](https://github.com/Ibjunior01/databoard-reports/actions/workflows/ci.yml/badge.svg)](https://github.com/Ibjunior01/databoard-reports/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![Tests](https://img.shields.io/badge/tests-206%20passed-success)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

**DataBoard Reports** é uma aplicação web em Python/Flask para upload, interpretação e análise automática de planilhas CSV e Excel.

O diferencial do projeto é a **inferência semântica de colunas**: em vez de depender apenas do `dtype` do Pandas ou de uma ordem fixa de campos, a aplicação analisa nomes, conteúdo, cardinalidade e padrões dos dados para classificar colunas e selecionar métricas, dimensões e visualizações mais adequadas.

O resultado é apresentado em um Dashboard interativo, com indicadores de qualidade dos dados, gráficos Plotly, histórico de uploads e geração de relatórios PDF.

---

## Principais recursos

- Upload seguro de arquivos `.csv`, `.xlsx` e `.xls`.
- Detecção automática de cabeçalho, inclusive quando ele não está na primeira linha.
- Processamento de planilhas sem depender de uma ordem fixa de colunas.
- Inferência semântica para:
  - identificadores;
  - datas e data/hora;
  - moedas;
  - percentuais;
  - quantidades;
  - métricas numéricas;
  - booleanos;
  - categorias;
  - texto livre;
  - campos desconhecidos.
- Proteção contra uso indevido de IDs, CEPs e códigos como métricas.
- Conversão analítica não destrutiva de valores como `R$ 1.250,00` e `13%`.
- Dashboard com:
  - seletor de uploads;
  - KPIs;
  - completude dos dados;
  - valores ausentes;
  - estrutura semântica identificada;
  - gráficos automáticos;
  - prévia dos dados;
  - ações rápidas.
- Gráficos automáticos de acordo com o contexto dos dados:
  - série temporal;
  - barras por categoria;
  - histograma;
  - dispersão entre métricas quando aplicável.
- Histórico de uploads e relatórios.
- Reprocessamento de planilhas já enviadas.
- Geração e download de relatórios PDF com ReportLab.
- Exclusão segura de uploads e arquivos relacionados.
- Tema claro/escuro persistido no navegador.
- Interface responsiva para desktop, tablet e mobile.
- Navegação por teclado e foco visível.
- CSRF em formulários POST.
- Headers HTTP básicos de segurança.
- Timezone configurável com armazenamento de timestamps em UTC.
- Docker + Gunicorn.
- CI com GitHub Actions para Ruff, Pytest e build Docker.

---

## Como funciona a análise automática

O DataBoard não assume que uma planilha precisa seguir um layout rígido.

O fluxo principal é:

```text
Upload CSV/XLS/XLSX
        ↓
Validação do arquivo
        ↓
Detecção do cabeçalho
        ↓
Carregamento com Pandas
        ↓
Perfil das colunas
        ↓
Inferência semântica
        ↓
Seleção de métricas e dimensões
        ↓
Análise estatística
        ↓
Gráficos automáticos
        ↓
Dashboard / Histórico / PDF
```

Exemplo de classificação:

```text
CLIENTE_ID     → IDENTIFIER
PEDIDO_ID      → IDENTIFIER
DATA_VENDA     → DATE
VALOR_TOTAL    → CURRENCY
QUANTIDADE     → QUANTITY
MARGEM_PCT     → PERCENTAGE
REGIAO         → CATEGORY
PRODUTO        → CATEGORY
ATIVO          → BOOLEAN
OBSERVACAO     → TEXT
```

A posição física das colunas não determina seu significado.

---

## Benchmark de autodetecção

O projeto possui uma planilha de benchmark em:

```text
tests/fixtures/databoard_autodetect_benchmark.xlsx
```

Ela cobre cenários como:

1. base realista;
2. mesmas colunas em ordem diferente;
3. tipos desafiadores armazenados como texto;
4. cabeçalho localizado na terceira linha.

Os testes verificam que a classificação semântica permanece consistente mesmo quando a ordem das colunas muda.

---

## Dashboard

O menu **Dashboard** funciona como uma central de análise.

Por padrão, ele abre o upload mais recente, mas o usuário pode selecionar qualquer arquivo registrado no histórico.

O Dashboard apresenta:

```text
KPIs
├── registros
├── colunas
├── métricas
├── categorias
└── valores ausentes

Qualidade dos dados
├── completude
├── total de valores ausentes
└── colunas afetadas

Estrutura detectada
├── métricas
├── categorias
├── datas
├── identificadores
├── booleanos
└── texto

Visualizações
├── gráficos automáticos
└── prévia dos dados
```

---

## Relatórios PDF

Os relatórios são gerados com **ReportLab** e podem incluir:

- informações do upload;
- data de upload e geração;
- resumo da análise;
- valores ausentes;
- estatísticas das métricas;
- prévia limitada da planilha;
- gráficos estáticos gerados a partir do Plotly/Kaleido.

Cada relatório fica associado ao upload de origem por meio do modelo `ReportRecord`.

---

## Stack

### Backend

- Python 3.12
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-WTF
- Pandas
- OpenPyXL
- xlrd

### Visualização e relatórios

- Plotly
- Kaleido
- ReportLab

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja
- Bootstrap 5

### Qualidade e infraestrutura

- Pytest
- Ruff
- Docker
- Gunicorn
- GitHub Actions
- Git / GitHub

---

## Arquitetura

O projeto utiliza Application Factory, Blueprint principal, camada de serviços e persistência com SQLAlchemy.

```text
databoard-reports/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── datetime_utils.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes.py
│   │
│   ├── services/
│   │   ├── analyzer.py
│   │   ├── charts.py
│   │   ├── data_loader.py
│   │   ├── history.py
│   │   ├── report_history.py
│   │   ├── reports.py
│   │   └── schema_inference.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   └── theme.css
│   │   └── js/
│   │       ├── theme-init.js
│   │       └── theme.js
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── index.html
│   │   ├── reports_history.html
│   │   ├── upload.html
│   │   └── upload_detail.html
│   │
│   ├── uploads/
│   └── reports/
│
├── tests/
│   ├── fixtures/
│   ├── test_analyzer.py
│   ├── test_charts.py
│   ├── test_dashboard.py
│   ├── test_data_loader.py
│   ├── test_datetime_utils.py
│   ├── test_history.py
│   ├── test_report_history.py
│   ├── test_reports.py
│   ├── test_schema_inference.py
│   ├── test_security_headers.py
│   └── test_upload.py
│
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── PROJECT_STATE.md
├── README.md
├── requirements.txt
└── run.py
```

---

## Segurança

A aplicação implementa medidas básicas para reduzir riscos comuns:

- `secure_filename()` no upload;
- nomes físicos únicos com UUID;
- limite máximo de upload;
- remoção de arquivos inválidos após falha;
- tratamento específico para planilhas corrompidas;
- proteção CSRF;
- `SECRET_KEY` obrigatória em produção;
- separação entre configurações de desenvolvimento, testes e produção;
- usuário não-root na imagem Docker;
- headers:
  - `X-Content-Type-Options: nosniff`;
  - `X-Frame-Options: DENY`;
  - `Referrer-Policy: strict-origin-when-cross-origin`;
  - `Permissions-Policy`.

> CSP e HSTS não foram habilitados nesta fase. HSTS depende de execução real em HTTPS, e uma CSP precisa considerar os recursos externos utilizados pelo frontend.

---

## Timezone

Os timestamps são gravados em UTC.

Na apresentação, o horário é convertido para o timezone configurado pela variável:

```text
APP_TIMEZONE
```

O padrão do projeto é:

```text
America/Fortaleza
```

---

## Executando localmente

Clone o repositório:

```bash
git clone https://github.com/Ibjunior01/databoard-reports.git
cd databoard-reports
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

No Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### Windows PowerShell

Configure o ambiente de desenvolvimento:

```powershell
$env:APP_ENV="development"
$env:SECRET_KEY="chave-local-de-desenvolvimento"
python run.py
```

### Linux/macOS

```bash
export APP_ENV=development
export SECRET_KEY="chave-local-de-desenvolvimento"
python run.py
```

Acesse:

```text
http://127.0.0.1:5000
```

---

## Variáveis de ambiente

| Variável | Uso | Exemplo |
|---|---|---|
| `APP_ENV` | Ambiente da aplicação | `development` |
| `SECRET_KEY` | Chave criptográfica do Flask | valor secreto |
| `APP_TIMEZONE` | Timezone de apresentação | `America/Fortaleza` |
| `UPLOAD_FOLDER` | Pasta persistente de uploads | `/data/uploads` |
| `REPORTS_FOLDER` | Pasta persistente de relatórios | `/data/reports` |
| `DATABASE_URL` | URI do banco SQLAlchemy | `sqlite:////data/databoard.sqlite3` |
| `PORT` | Porta usada pelo Gunicorn | `5000` |

Nunca versione uma `SECRET_KEY` de produção.

---

## Testes e lint

Execute a suíte:

```bash
python -m pytest
```

Resultado atual:

```text
206 passed
```

Execute o lint:

```bash
python -m ruff check .
```

Resultado esperado:

```text
All checks passed!
```

Os testes cobrem, entre outros pontos:

- upload e validação;
- arquivos inválidos;
- limite de tamanho;
- detecção de cabeçalho;
- benchmark de autodetecção;
- inferência semântica;
- análise automática;
- seleção de gráficos;
- histórico;
- relatórios PDF;
- timezone;
- CSRF;
- headers de segurança;
- Dashboard e seletor de uploads.

---

## CI com GitHub Actions

O workflow:

```text
.github/workflows/ci.yml
```

é executado em pushes e pull requests para `main`.

Os jobs validam:

```text
Ruff
Pytest
Docker build
```

O objetivo é impedir regressões de qualidade antes da integração de novas mudanças.

---

## Docker

Construa a imagem:

```bash
docker build -t databoard-reports .
```

Execute localmente:

```bash
docker run --rm \
  -e APP_ENV=production \
  -e SECRET_KEY="chave-local-de-teste" \
  -p 5000:5000 \
  databoard-reports
```

O container utiliza Gunicorn e aceita a variável `PORT`:

```text
${PORT:-5000}
```

A imagem é executada com usuário não-root.

---

## Persistência

Por padrão, o ambiente local utiliza SQLite e diretórios locais para uploads e relatórios.

A aplicação também permite externalizar os caminhos por variáveis de ambiente:

```text
DATABASE_URL
UPLOAD_FOLDER
REPORTS_FOLDER
```

Isso deixa o projeto preparado para um ambiente com armazenamento persistente.

---

## Acessibilidade e interface

A interface possui:

- layout responsivo;
- tema claro e escuro;
- preferência de tema persistida em `localStorage`;
- suporte a `prefers-color-scheme`;
- foco visível;
- navegação por teclado;
- skip link;
- suporte a `prefers-reduced-motion`;
- tabelas adaptadas para mobile;
- gráficos sincronizados com o tema.

Na auditoria local com Lighthouse, **Accessibility** e **Best Practices** atingiram 100 em Desktop e Mobile.

---

## Deploy

O projeto está preparado para deploy com Docker/Gunicorn e configuração por variáveis de ambiente.

Nesta versão do portfólio, **não há uma demonstração pública hospedada**. A aplicação pode ser executada localmente ou implantada posteriormente em uma infraestrutura compatível com armazenamento persistente.

---

## Status do projeto

Versão atual considerada estável para portfólio:

```text
✓ upload CSV/XLS/XLSX
✓ autodetecção de cabeçalho
✓ inferência semântica
✓ análise automática
✓ Dashboard interativo
✓ gráficos automáticos
✓ histórico
✓ relatórios PDF
✓ exclusões seguras
✓ tema claro/escuro
✓ responsividade
✓ segurança básica
✓ Docker/Gunicorn
✓ GitHub Actions
✓ Ruff limpo
✓ 206 testes
```

Evoluções futuras possíveis:

- autenticação e autorização;
- paginação de históricos;
- filtros analíticos avançados;
- banco PostgreSQL em produção;
- object storage para arquivos;
- Content Security Policy;
- deploy público;
- observabilidade e monitoramento.

---

## Objetivo profissional

Este projeto foi desenvolvido para estudo e portfólio, com foco em demonstrar competências em:

- desenvolvimento web com Flask;
- processamento de dados com Pandas;
- modelagem e persistência com SQLAlchemy;
- inferência baseada em heurísticas;
- visualização de dados;
- testes automatizados;
- segurança de aplicações web;
- Docker;
- CI/CD;
- responsividade e acessibilidade;
- organização incremental de um projeto de software.

---

## Licença

Projeto desenvolvido para fins educacionais, demonstração técnica e portfólio profissional.
