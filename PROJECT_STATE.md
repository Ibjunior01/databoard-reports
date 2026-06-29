# PROJECT_STATE.md

## Projeto

DataBoard Reports

## Repositório local sugerido

spreadsheet-dashboard-platform

## Repositório GitHub sugerido

databoard-reports

## Descrição geral

O DataBoard Reports será uma plataforma web desenvolvida em Python com Flask para permitir que empresas façam upload de planilhas CSV ou Excel, visualizem dashboards automáticos, gerem gráficos interativos e exportem relatórios em PDF.

O projeto está sendo construído em entregas pequenas e sequenciais, com foco em portfólio profissional para GitHub e divulgação no LinkedIn.

## Stack principal planejada

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

## Identidade visual definida

O projeto seguirá uma identidade visual dark/profissional, inspirada em dashboards SaaS modernos.

### Direção visual

- Fundo principal em azul muito escuro/preto técnico.
- Cards em tons de slate/navy.
- Azul claro como cor primária de ação.
- Bordas discretas.
- Sombras suaves para profundidade.
- Layout limpo, profissional e adequado para portfólio.

### Paleta base

- Background principal: `#020617`
- Superfície/card: `#0f172a`
- Superfície secundária: `#111827`
- Bordas: `#1e293b`
- Texto principal: `#f8fafc`
- Texto secundário: `#94a3b8`
- Azul primário: `#38bdf8`
- Azul hover: `#0ea5e9`

### Regra de design

Todas as próximas telas devem seguir a paleta dark definida, evitando páginas com fundo branco puro. A interface deve manter aparência de produto SaaS profissional voltado para análise de dados e dashboards empresariais.

## Entrega atual

Conversa 4 — Exibição da prévia dos dados na interface web

## Objetivo da entrega atual

Integrar a camada de leitura de planilhas com o fluxo de upload, permitindo que o sistema exiba no navegador os metadados e uma prévia dos dados carregados.

## O que já foi implementado

### Conversa 1 — Base inicial Flask

* Estrutura inicial de pastas criada.
* Application factory do Flask criada.
* Página inicial criada.
* Template base criado.
* CSS inicial criado.
* Arquivo de configuração centralizado criado.
* Arquivo requirements.txt criado.
* Arquivo .gitignore criado.
* Arquivo .env.example criado.
* Dockerfile inicial criado.
* docker-compose.yml inicial criado.
* README.md inicial criado.
* PROJECT_STATE.md criado.
* Arquivos placeholder da camada de services criados.
* Pastas uploads, reports e sample_data criadas.
* Arquivo conftest.py criado para corrigir importações no Pytest.
* Testes iniciais criados.
* O comando python run.py funcionou.
* A aplicação abriu corretamente em http://127.0.0.1:5000.
* O comando python -m pytest retornou testes passando.

### Conversa 2 — Upload inicial de arquivos CSV e Excel

* Rota GET /upload criada.
* Rota POST /upload criada.
* Link Upload ativado no menu do base.html.
* Tela profissional de upload criada em upload.html.
* Formulário HTML criado com enctype="multipart/form-data".
* Validação de extensões permitidas criada.
* Extensões permitidas nesta etapa:

  * .csv
  * .xlsx
  * .xls
* Arquivos inválidos são recusados antes do salvamento.
* Função secure_filename do Werkzeug aplicada ao nome do arquivo.
* Arquivos enviados são salvos em app/uploads/.
* Mensagens de sucesso e erro foram implementadas com flash.
* CSS da tela de upload foi ajustado para uma identidade visual mais dark/profissional.
* Testes básicos para extensões permitidas foram criados.
* Teste básico para GET /upload com status 200 foi criado.
* Teste de upload válido .csv criado.
* Teste de bloqueio para arquivo inválido .pdf criado.
* O comando python -m pytest retornou 13 passed.
* README.md atualizado.
* PROJECT_STATE.md atualizado.

### Conversa 3 — Leitura inicial de arquivos com Pandas

* Arquivo app/services/data_loader.py atualizado.
* Criada constante SUPPORTED_EXTENSIONS com:

  * .csv
  * .xlsx
  * .xls
* Criada constante DEFAULT_PREVIEW_ROWS.
* Criada exceção UnsupportedFileTypeError para extensões não suportadas.
* Criada estrutura SpreadsheetMetadata usando dataclass.
* Criada função get_file_extension.
* Criada função allowed_file.
* Criada função validate_file_path.
* Criada função load_spreadsheet.
* Criada função build_spreadsheet_metadata.
* Criada função load_spreadsheet_metadata.
* Criadas funções de compatibilidade:

  * read_spreadsheet
  * get_spreadsheet_metadata
* Implementada leitura de arquivos .csv com Pandas.
* Implementada leitura de arquivos .xlsx com Pandas e openpyxl.
* Implementada leitura de arquivos .xls com Pandas e xlrd.
* Implementada validação de existência do arquivo antes da leitura.
* Implementada validação de extensão suportada.
* Implementado retorno de metadados básicos:

  * nome do arquivo;
  * extensão do arquivo;
  * quantidade de linhas;
  * quantidade de colunas;
  * nomes das colunas;
  * prévia das primeiras linhas.
* Arquivo tests/test_data_loader.py atualizado.
* Criados testes para validação de extensões suportadas.
* Criados testes para rejeição de extensões não suportadas.
* Criados testes para leitura de CSV.
* Criados testes para leitura de Excel.
* Criados testes para metadados de CSV.
* Criados testes para metadados de Excel.
* Criado teste para arquivo inexistente.
* Criado teste para extensão não suportada.
* Criado teste para controle de quantidade de linhas na prévia.
* README.md atualizado.
* PROJECT_STATE.md atualizado.
* requirements.txt atualizado com dependências necessárias para leitura de Excel:

  * openpyxl
  * xlrd

### Conversa 4 — Exibição da prévia dos dados na interface web

- Rota POST /upload integrada com a leitura de planilhas.
- Arquivo enviado é salvo e imediatamente carregado com Pandas.
- Função load_spreadsheet_metadata utilizada no fluxo web.
- Template dashboard.html atualizado para exibir metadados.
- Exibição do nome do arquivo.
- Exibição da extensão do arquivo.
- Exibição da quantidade de linhas.
- Exibição da quantidade de colunas.
- Exibição dos nomes das colunas.
- Exibição das primeiras linhas da planilha.
- Ajuste dos nomes dos campos conforme a dataclass SpreadsheetMetadata:
  - file_name
  - file_extension
  - rows
  - columns
  - column_names
  - preview
- Correção das rotas para usar main.upload_file.
- Fixture global client configurada no conftest.py.
- Teste de upload com exibição de metadados criado.
- Testes ajustados para o novo fluxo de upload.
- O comando python -m pytest retornou 15 passed.

### Conversa 5 — Análise automática inicial dos dados carregados

* Arquivo app/services/analyzer.py atualizado.
* Criada estrutura DataAnalysisResult usando dataclass.
* Criada função analyze_dataframe.
* Implementada identificação de colunas numéricas.
* Implementada identificação de colunas categóricas/texto.
* Implementada contagem de valores ausentes por coluna.
* Implementado cálculo percentual de valores ausentes por coluna.
* Implementada contagem de valores únicos por coluna.
* Implementado cálculo de estatísticas básicas para colunas numéricas:
  * média;
  * mínimo;
  * máximo;
  * mediana.
* Implementado tratamento para DataFrame vazio.
* Implementada validação para rejeitar entradas que não sejam pandas.DataFrame.
* Arquivo tests/test_analyzer.py atualizado.
* Criados testes unitários para a camada de análise.
* O comando python -m pytest retornou 23 passed.

## Estrutura atual esperada

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

## Arquivos modificados na Conversa 5

app/services/analyzer.py
tests/test_analyzer.py
README.md
PROJECT_STATE.md

## Comando para executar a aplicação

```bash
python run.py
```

## Comando para executar os testes

```bash
python -m pytest
```

## Resultado esperado dos testes

O comando abaixo deve retornar todos os testes passando:
python -m pytest
Resultado validado na Conversa 5:
23 passed

## O que ainda não foi implementado

* Exibição da análise automática no dashboard.
* Gráficos interativos.
* Banco de dados.
* SQLAlchemy.
* Histórico de uploads.
* Geração de PDF.
* Autenticação.
* Deploy.
* Pipeline CI/CD.

## Próxima entrega sugerida

Conversa 6 — Exibição da análise automática no dashboard.

## Objetivo provável da Conversa 6

Integrar a camada de análise automática com o fluxo de upload, permitindo que o sistema exiba no dashboard web informações estruturadas sobre os dados carregados.

## Escopo recomendado para a Conversa 6

Integrar a função analyze_dataframe() na rota de upload.

Enviar o resultado da análise para o template dashboard.html.

Exibir cards com informações gerais:

total de linhas;
total de colunas;
quantidade de colunas numéricas;
quantidade de colunas categóricas.

Exibir lista de colunas numéricas.

Exibir lista de colunas categóricas/texto.

Exibir tabela de valores ausentes por coluna:

nome da coluna;
quantidade de valores ausentes;
percentual de valores ausentes.

Exibir estatísticas básicas das colunas numéricas:

média;
mínimo;
máximo;
mediana.

Ajustar o layout do dashboard.html seguindo a identidade visual dark/profissional definida para o DataBoard Reports.

Adicionar ou ajustar testes para garantir que o dashboard exibe os dados da análise automática.

Manter fora do escopo nesta etapa:

gráficos interativos;
Plotly;
banco de dados;
histórico de uploads;
geração de PDF;
autenticação;
deploy.

Observação de continuidade

A Conversa 5 concluiu a criação da camada de análise automática dos dados carregados. O projeto agora possui uma função desacoplada da interface web capaz de analisar um DataFrame e retornar informações estruturadas sobre colunas, valores ausentes, valores únicos e estatísticas numéricas.

A partir da Conversa 6, o projeto deve evoluir para exibir essa análise diretamente no dashboard, mantendo a identidade visual dark/profissional definida para o DataBoard Reports.
