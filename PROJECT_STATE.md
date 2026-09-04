# PROJECT_STATE.md

## Projeto

**DataBoard Reports**

---

## Estado atual

O DataBoard Reports está em uma versão **estável para portfólio**, com o núcleo funcional concluído, testes automatizados, CI, Docker, segurança básica, responsividade, tema claro/escuro e documentação técnica.

Estado validado:

```text
206 testes aprovados
Ruff sem erros
GitHub Actions aprovado
Docker build aprovado
Gunicorn validado
Tema claro/escuro validado
Responsividade validada
Accessibility 100
Best Practices 100
```

O deploy público foi preparado tecnicamente, mas **não será realizado nesta fase**.

---

## Objetivo do projeto

Criar uma aplicação web profissional capaz de receber planilhas CSV e Excel, interpretar automaticamente sua estrutura, identificar semanticamente o papel das colunas e transformar os dados em análises, indicadores, gráficos e relatórios PDF.

O projeto foi desenvolvido com foco em:

- engenharia de software;
- separação de responsabilidades;
- testes automatizados;
- segurança básica;
- análise de dados;
- UX responsiva;
- acessibilidade;
- Docker;
- CI/CD;
- documentação profissional;
- preparação para portfólio.

---

## Diferencial principal

O DataBoard Reports não depende de uma ordem fixa de colunas.

A aplicação utiliza um motor de inferência semântica para identificar o significado provável dos campos com base em:

- nome da coluna;
- tipo Pandas;
- conteúdo;
- padrões textuais;
- cardinalidade;
- valores únicos;
- proporção de nulos;
- contexto semântico.

Tipos semânticos suportados:

```text
IDENTIFIER
DATETIME
DATE
PERCENTAGE
CURRENCY
BOOLEAN
QUANTITY
NUMERIC
CATEGORY
TEXT
UNKNOWN
```

Exemplo:

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

Identificadores, CEPs e códigos não são utilizados automaticamente como métricas.

---

## Stack atual

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
- Git
- GitHub
- Visual Studio Code

---

## Estrutura principal

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
│   │   └── databoard_autodetect_benchmark.xlsx
│   ├── conftest.py
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

## Arquitetura

A aplicação utiliza uma organização em camadas.

### Apresentação

Responsável pela interface:

```text
app/templates/
app/static/
```

### Rotas

Responsável por receber requisições HTTP e coordenar os serviços:

```text
app/routes.py
```

### Serviços

Responsáveis pelas regras de negócio:

```text
app/services/data_loader.py
app/services/schema_inference.py
app/services/analyzer.py
app/services/charts.py
app/services/history.py
app/services/report_history.py
app/services/reports.py
```

### Persistência

Responsável por banco e modelos:

```text
app/models.py
app/extensions.py
app/config.py
```

### Testes

Responsáveis pela validação automatizada:

```text
tests/
```

---

## Application Factory

A aplicação utiliza Application Factory por meio de:

```python
create_app()
```

Configurações separadas:

```text
Config
DevelopmentConfig
TestingConfig
ProductionConfig
```

`APP_ENV` determina o ambiente.

Produção exige uma `SECRET_KEY` válida.

---

## Upload de arquivos

Formatos permitidos:

```text
.csv
.xlsx
.xls
```

Recursos implementados:

- `secure_filename()`;
- nomes físicos únicos com UUID;
- limite máximo de upload;
- validação de extensão;
- tratamento de arquivo inexistente;
- tratamento de planilhas corrompidas;
- remoção automática de upload inválido;
- mensagem amigável para erro de processamento;
- tratamento HTTP 413.

Os nomes exibidos ao usuário permanecem os nomes originais.

---

## Detecção automática de cabeçalho

O carregador procura o cabeçalho nas primeiras linhas da planilha.

O benchmark valida:

```text
01_Base_Realista
→ cabeçalho na primeira linha

02_Colunas_Reordenadas
→ cabeçalho na primeira linha

03_Tipos_Desafiadores
→ cabeçalho na primeira linha

04_Cabecalho_Linha3
→ cabeçalho na terceira linha
```

A planilha de benchmark não foi alterada para fazer os testes passarem.

---

## Benchmark oficial

Arquivo:

```text
tests/fixtures/databoard_autodetect_benchmark.xlsx
```

Cenários:

### 01_Base_Realista

```text
VENDEDOR       → CATEGORY
CLIENTE_ID     → IDENTIFIER
DATA_VENDA     → DATE
REGIAO         → CATEGORY
VALOR_TOTAL    → CURRENCY
PEDIDO_ID      → IDENTIFIER
QUANTIDADE     → QUANTITY
PRODUTO        → CATEGORY
MARGEM_PCT     → PERCENTAGE
ATIVO          → BOOLEAN
```

### 02_Colunas_Reordenadas

Mesma semântica da primeira aba, independentemente da ordem física.

### 03_Tipos_Desafiadores

```text
CODIGO_CLIENTE → IDENTIFIER
DATA           → DATE
FATURAMENTO    → CURRENCY
DESCONTO       → PERCENTAGE
CATEGORIA      → CATEGORY
CEP            → IDENTIFIER
OBSERVACAO     → TEXT
```

### 04_Cabecalho_Linha3

```text
DATA       → DATE
UNIDADE    → CATEGORY
SERVICO    → CATEGORY
QTD        → QUANTITY
RECEITA    → CURRENCY
STATUS     → CATEGORY
```

---

## Inferência semântica

Arquivo:

```text
app/services/schema_inference.py
```

Principais responsabilidades:

- normalização de nomes;
- criação de perfil de coluna;
- amostragem;
- score por tipo;
- classificação final;
- classificação do DataFrame inteiro.

Princípio fundamental:

```text
posição da coluna ≠ significado da coluna
```

---

## Analyzer

Arquivo:

```text
app/services/analyzer.py
```

O analyzer utiliza o motor semântico.

Mantém compatibilidade com campos históricos da aplicação, mas separa:

```text
identifier_columns
datetime_columns
date_columns
percentage_columns
currency_columns
boolean_columns
quantity_columns
metric_columns
category_columns
text_columns
unknown_columns
```

Também calcula:

- valores ausentes;
- percentual de ausentes;
- valores únicos;
- estatísticas numéricas;
- métricas semanticamente válidas.

Conversões analíticas são não destrutivas.

Exemplos:

```text
"R$ 1.250,00" → 1250.00 para cálculo
"13%"         → 13.0 para cálculo
```

O DataFrame original não é alterado.

---

## Gráficos automáticos

Arquivo:

```text
app/services/charts.py
```

Seleção semântica:

```text
DATE/DATETIME + métrica
→ série temporal

CATEGORY + métrica
→ barras agregadas

1 métrica
→ histograma

2 métricas
→ dispersão quando aplicável

CATEGORY sem métrica
→ distribuição por barras
```

Regras:

- identificadores não viram métricas;
- texto livre não é plotado automaticamente;
- categorias de cardinalidade excessiva são evitadas;
- limite de gráficos automáticos preserva clareza da interface.

Plotly acompanha o tema claro/escuro.

---

## Dashboard

O Dashboard foi transformado em central de análise.

Rota:

```text
GET /dashboard
GET /dashboard?upload_id=<id>
```

Comportamento:

```text
sem uploads
→ estado vazio

com uploads
→ abre o mais recente

upload_id informado
→ abre o upload selecionado
```

Recursos:

- seletor de upload;
- arquivo atual;
- KPIs;
- registros;
- colunas;
- métricas;
- categorias;
- valores ausentes;
- completude;
- colunas afetadas;
- estrutura semântica;
- gráficos;
- prévia;
- ações rápidas.

Ações rápidas:

```text
Gerar PDF
Ver detalhes
Histórico
Novo upload
```

---

## Qualidade dos dados

O Dashboard apresenta:

```text
completude
total de valores ausentes
quantidade de colunas afetadas
```

Exemplo validado com benchmark:

```text
240 registros
10 colunas
3 métricas
13 valores ausentes
```

---

## Histórico de uploads

Implementado:

- persistência com SQLAlchemy;
- ordenação por data/ID;
- detalhes;
- reprocessamento;
- exclusão;
- remoção do arquivo físico;
- remoção de relatórios vinculados;
- cascata;
- confirmação na interface;
- CSRF;
- tratamento de arquivos ausentes.

No mobile/tablet, registros são exibidos em cards responsivos.

---

## Relatórios

Modelo:

```text
ReportRecord
```

Recursos:

- geração de PDF;
- histórico de relatórios;
- associação ao upload;
- download posterior;
- exclusão individual;
- exclusão física;
- tratamento de arquivo ausente;
- CSRF.

---

## PDF

Arquivo:

```text
app/services/reports.py
```

Conteúdo:

- dados do upload;
- data do upload;
- data de geração;
- resumo;
- valores ausentes;
- estatísticas;
- prévia;
- gráficos.

Melhorias realizadas:

- quebra correta de textos longos;
- cabeçalhos legíveis;
- prévia limitada para A4;
- gráficos estáticos;
- timezone consistente.

---

## Modelos persistentes

### UploadRecord

Campos principais:

```text
id
file_name
file_extension
file_path
row_count
column_count
created_at
```

Relacionamento:

```text
UploadRecord 1 ─── N ReportRecord
```

### ReportRecord

Campos principais:

```text
id
upload_id
file_name
file_path
created_at
```

Relacionamento configurado com exclusão em cascata.

---

## Timezone

Timestamps são armazenados em UTC.

Na apresentação são convertidos para:

```text
APP_TIMEZONE
```

Padrão:

```text
America/Fortaleza
```

Utilitário:

```text
app/datetime_utils.py
```

---

## Tema claro/escuro

Arquivos:

```text
app/static/css/theme.css
app/static/js/theme-init.js
app/static/js/theme.js
```

Recursos:

- tema claro;
- tema escuro;
- persistência via `localStorage`;
- `prefers-color-scheme`;
- redução de flash de tema;
- sincronização com Plotly;
- suporte a `prefers-reduced-motion`.

---

## Responsividade

Validada em:

- desktop;
- tablet;
- mobile;
- viewport de 375 × 667.

Históricos mudam de tabela para cards abaixo de `1199.98px`.

A prévia permite scroll horizontal apenas dentro da tabela, sem gerar scroll lateral da página.

---

## Acessibilidade

Implementado:

- navegação por teclado;
- foco visível;
- skip link;
- labels;
- `scope` em cabeçalhos;
- alvos de toque;
- `prefers-reduced-motion`;
- estrutura semântica;
- botão de tema acessível;
- menu mobile acessível.

Lighthouse local:

```text
Desktop
Accessibility: 100
Best Practices: 100

Mobile
Accessibility: 100
Best Practices: 100
```

---

## Segurança

Implementado:

- configuração por ambiente;
- `SECRET_KEY` obrigatória em produção;
- CSRF;
- upload validado;
- UUID para nomes físicos;
- limite de arquivo;
- limpeza de inválidos;
- usuário Docker não-root;
- ações destrutivas via POST;
- confirmação de exclusões;
- logs de falhas;
- headers HTTP.

Headers:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

Ainda não implementados:

```text
Content-Security-Policy
Strict-Transport-Security
```

Motivos:

- CSP precisa considerar Bootstrap/Plotly;
- HSTS depende de HTTPS real em produção.

---

## Docker

Dockerfile normalizado e validado.

Características:

- Python slim;
- dependências instaladas por `requirements.txt`;
- usuário não-root;
- Gunicorn;
- 2 workers;
- timeout 120 s;
- porta dinâmica.

Execução:

```text
${PORT:-5000}
```

Build local validado.

Container validado em porta 8080.

---

## Persistência configurável

Variáveis:

```text
UPLOAD_FOLDER
REPORTS_FOLDER
DATABASE_URL
```

Isso permite mover:

```text
SQLite
uploads
reports
```

para storage persistente em um ambiente de produção.

---

## CI

Workflow:

```text
.github/workflows/ci.yml
```

Executado em:

```text
push → main
pull_request → main
```

Jobs:

```text
Ruff and Pytest
Docker build
```

Ambos foram validados com sucesso no GitHub Actions.

---

## Testes

Comando:

```bash
python -m pytest
```

Resultado atual:

```text
206 passed
```

Lint:

```bash
python -m ruff check .
```

Resultado:

```text
All checks passed!
```

Cobertura funcional inclui:

- upload;
- CSV/XLS/XLSX;
- arquivos inválidos;
- limite de tamanho;
- cleanup;
- autodetecção de cabeçalho;
- benchmark;
- inferência semântica;
- analyzer;
- gráficos;
- histórico;
- reprocessamento;
- exclusão;
- PDF;
- persistência de relatório;
- timezone;
- CSRF;
- headers;
- Dashboard;
- seletor de uploads.

---

## Rotas principais

```text
GET  /
GET  /upload
POST /upload

GET  /dashboard
GET  /dashboard?upload_id=<id>

GET  /history
GET  /history/<record_id>
GET  /history/<record_id>/reprocess
GET  /history/<record_id>/report
POST /history/<record_id>/delete

GET  /reports
GET  /reports/<report_id>/download
POST /reports/<report_id>/delete
```

---

## Decisões técnicas

### Manter Flask

O projeto continuará usando Flask.

### Manter Pandas

Pandas permanece responsável pelo carregamento e preparação dos dados.

### Manter SQLAlchemy

SQLite é suficiente para a versão local/portfólio.

### Não realizar deploy nesta fase

A aplicação está preparada para deploy, mas não será hospedada publicamente nesta versão.

### Não migrar agora para PostgreSQL

A migração só é necessária quando houver requisito real de produção multiusuário ou infraestrutura externa.

### Não aumentar escopo do Dashboard

O Dashboard atual atende ao objetivo de portfólio.

Filtros avançados e BI customizável ficam como evolução futura.

---

## Funcionalidades concluídas

```text
✓ Flask Application Factory
✓ configuração por ambiente
✓ CSV/XLS/XLSX
✓ upload seguro
✓ cabeçalho automático
✓ benchmark
✓ inferência semântica
✓ analyzer semântico
✓ gráficos semânticos
✓ Dashboard
✓ seletor de uploads
✓ KPIs
✓ qualidade dos dados
✓ histórico
✓ detalhes
✓ reprocessamento
✓ PDF
✓ histórico de relatórios
✓ exclusões seguras
✓ CSRF
✓ timezone
✓ tema claro/escuro
✓ responsividade
✓ acessibilidade
✓ headers de segurança
✓ Docker
✓ Gunicorn
✓ Ruff
✓ Pytest
✓ GitHub Actions
✓ 206 testes
```

---

## Fora do escopo da versão atual

Não são necessários para considerar o projeto concluído:

- autenticação;
- autorização;
- multiusuário;
- paginação;
- busca avançada;
- filtros analíticos;
- upload múltiplo;
- API REST;
- PostgreSQL;
- object storage;
- observabilidade;
- monitoramento;
- backup automatizado;
- deploy público.

---

## Evoluções futuras possíveis

Se o projeto voltar a evoluir:

1. autenticação;
2. PostgreSQL;
3. object storage;
4. paginação;
5. filtros;
6. persistência da análise;
7. API REST;
8. CSP;
9. observabilidade;
10. deploy público.

---

## Regras de continuidade

Caso o desenvolvimento seja retomado:

- preservar os 206 testes;
- manter Ruff limpo;
- adicionar testes para novos comportamentos;
- evitar regressões no benchmark;
- não usar posição de coluna para inferir significado;
- não transformar identificadores em métricas;
- manter ações destrutivas via POST;
- manter CSRF;
- preservar Application Factory;
- manter separação entre rotas, serviços, modelos e templates;
- executar CI antes de considerar uma entrega concluída.

---

## Status final para portfólio

O projeto está considerado:

```text
ESTÁVEL
TESTADO
DOCUMENTADO
DOCKERIZADO
RESPONSIVO
ACESSÍVEL
PREPARADO PARA DEPLOY
PRONTO PARA PORTFÓLIO
```

O deploy público permanece opcional.

---

## Próxima etapa do projeto

A próxima etapa não é adicionar funcionalidades.

A sequência recomendada é:

```text
PROJECT_STATE atualizado
→ padronização final do repositório
→ revisão do GitHub
→ screenshots
→ vídeo demonstrativo
→ inclusão no portfólio
```
