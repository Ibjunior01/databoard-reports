````markdown
# PROJECT_STATE.md

## Projeto

DataBoard Reports

## Descrição

DataBoard Reports é uma aplicação web desenvolvida em Python com Flask para envio, processamento e análise automática de planilhas CSV, XLSX e XLS.

A aplicação utiliza Pandas para leitura e análise dos dados, Plotly para geração de gráficos interativos, SQLite com SQLAlchemy para persistência e ReportLab para criação de relatórios PDF.

O projeto está sendo desenvolvido em entregas pequenas e sequenciais, com foco em:

* boas práticas de engenharia de software;
* separação de responsabilidades;
* testes automatizados;
* organização profissional do repositório;
* evolução incremental;
* preparação para portfólio no GitHub;
* futura implantação em ambiente de produção.

---

## Objetivo do projeto

Criar uma plataforma web profissional capaz de:

* receber arquivos CSV, XLSX e XLS;
* validar os arquivos enviados;
* armazenar os arquivos no servidor;
* carregar os dados com Pandas;
* identificar a estrutura da planilha;
* exibir uma prévia dos dados;
* identificar colunas numéricas e categóricas;
* calcular valores ausentes;
* gerar estatísticas automáticas;
* criar gráficos interativos;
* registrar uploads no banco de dados;
* consultar o histórico de uploads;
* reprocessar planilhas já enviadas;
* gerar relatórios PDF;
* persistir os relatórios gerados;
* consultar o histórico de relatórios;
* baixar novamente relatórios existentes;
* excluir relatórios com segurança;
* excluir uploads e arquivos relacionados;
* evoluir futuramente para autenticação, filtros, paginação e deploy.

---

## Entrega atual

Conversa 20 — Exclusão segura de uploads e arquivos associados

## Objetivo da entrega atual

Permitir a exclusão completa e segura de um upload, removendo:

* o arquivo original da planilha;
* os arquivos PDF relacionados;
* os registros de relatórios;
* o registro do upload.

A exclusão utiliza requisição `POST`, confirmação na interface e relacionamento em cascata entre uploads e relatórios.

---

## Stack atual

* Python
* Flask
* Pandas
* Plotly
* SQLite
* Flask-SQLAlchemy
* SQLAlchemy
* ReportLab
* HTML
* CSS
* Jinja
* Bootstrap
* Pytest
* Git
* GitHub
* Visual Studio Code

---

## Stack planejada

* Docker
* Flask-Migrate
* CI/CD
* Deploy em nuvem
* Banco PostgreSQL em produção
* Autenticação e autorização
* Proteção CSRF

---

## Estrutura atual esperada

```text
databoard-reports/
│
├── app/
│   ├── __init__.py
│   ├── config.py
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
│   │   └── reports.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── upload_detail.html
│   │   └── reports_history.html
│   │
│   ├── uploads/
│   └── reports/
│
├── instance/
│   └── databoard.db
│
├── tests/
│   ├── conftest.py
│   ├── test_analyzer.py
│   ├── test_charts.py
│   ├── test_data_loader.py
│   ├── test_history.py
│   ├── test_reports.py
│   ├── test_report_history.py
│   ├── test_routes.py
│   └── test_upload.py
│
├── PROJECT_STATE.md
├── README.md
├── requirements.txt
├── run.py
└── .gitignore
```

---

## Arquitetura atual

A aplicação utiliza uma organização baseada em camadas.

### Camada de apresentação

Responsável pela interface da aplicação.

Arquivos principais:

* `app/templates/base.html`
* `app/templates/index.html`
* `app/templates/upload.html`
* `app/templates/dashboard.html`
* `app/templates/history.html`
* `app/templates/upload_detail.html`
* `app/templates/reports_history.html`
* `app/static/css/style.css`

### Camada de rotas

Responsável por receber as requisições HTTP e coordenar os serviços.

Arquivo principal:

* `app/routes.py`

### Camada de serviços

Responsável pelas regras de negócio e operações específicas.

Arquivos principais:

* `app/services/data_loader.py`
* `app/services/analyzer.py`
* `app/services/charts.py`
* `app/services/history.py`
* `app/services/report_history.py`
* `app/services/reports.py`

### Camada de persistência

Responsável pelos modelos e acesso ao banco de dados.

Arquivos principais:

* `app/models.py`
* `app/extensions.py`
* `app/config.py`

### Camada de testes

Responsável pela validação automática do comportamento da aplicação.

Arquivos principais:

* `tests/conftest.py`
* `tests/test_analyzer.py`
* `tests/test_charts.py`
* `tests/test_data_loader.py`
* `tests/test_history.py`
* `tests/test_reports.py`
* `tests/test_report_history.py`
* `tests/test_routes.py`
* `tests/test_upload.py`

---

## Modelos persistentes atuais

### UploadRecord

Representa uma planilha enviada para a aplicação.

Campos:

* `id`
* `file_name`
* `file_extension`
* `file_path`
* `row_count`
* `column_count`
* `created_at`

Relacionamento:

* um upload pode possuir vários relatórios;
* relacionamento configurado com `cascade="all, delete-orphan"`.

### ReportRecord

Representa um relatório PDF gerado.

Campos:

* `id`
* `upload_id`
* `file_name`
* `file_path`
* `created_at`

Relacionamento:

* cada relatório pertence a um upload.

---

## O que já foi implementado

### Estrutura inicial da aplicação

* Projeto Flask criado.
* Application factory configurada.
* Blueprint principal criado.
* Configuração centralizada criada.
* Pasta de templates criada.
* Pasta de arquivos estáticos criada.
* Estrutura de serviços criada.
* Ambiente de testes com Pytest configurado.
* Banco SQLite de testes em memória configurado.

### Upload de planilhas

* Formulário de upload criado.
* Upload de arquivos CSV implementado.
* Upload de arquivos XLSX implementado.
* Upload de arquivos XLS implementado.
* Validação de extensão implementada.
* Uso de `secure_filename()` implementado.
* Criação automática da pasta de uploads implementada.
* Salvamento do arquivo físico implementado.
* Mensagens de sucesso e erro adicionadas.

### Carregamento dos dados

* Serviço de carregamento com Pandas criado.
* Leitura de CSV implementada.
* Leitura de XLSX implementada.
* Leitura de XLS implementada.
* Exceção `UnsupportedFileTypeError` criada.
* Validação de arquivo inexistente implementada.
* Extração de metadados implementada.

### Metadados da planilha

* Nome do arquivo extraído.
* Extensão do arquivo extraída.
* Quantidade de linhas calculada.
* Quantidade de colunas calculada.
* Nomes das colunas extraídos.
* Prévia das primeiras linhas criada.

### Análise automática

* Serviço `analyzer.py` criado.
* Identificação de colunas numéricas implementada.
* Identificação de colunas categóricas implementada.
* Contagem de valores ausentes implementada.
* Percentual de valores ausentes implementado.
* Contagem de valores únicos implementada.
* Estatísticas numéricas básicas implementadas.
* Resultado da análise organizado para o dashboard.

### Gráficos automáticos

* Serviço `charts.py` criado.
* Histogramas para colunas numéricas implementados.
* Gráficos de barras para colunas categóricas implementados.
* Gráficos Plotly integrados ao dashboard.
* Geração de imagens de gráficos para PDF implementada.
* Tratamento para planilhas sem colunas adequadas implementado.

### Dashboard

* Página de dashboard criada.
* Metadados exibidos.
* Colunas da planilha exibidas.
* Prévia dos dados exibida.
* Análise automática exibida.
* Estatísticas numéricas exibidas.
* Valores ausentes exibidos.
* Gráficos interativos exibidos.
* Estado vazio do dashboard implementado.
* Layout responsivo criado.

### Histórico de uploads

* SQLite integrado à aplicação.
* Flask-SQLAlchemy configurado.
* Instância global `db` criada.
* Modelo `UploadRecord` criado.
* Registro automático de uploads implementado.
* Serviço `history.py` criado.
* Consulta dos uploads mais recentes implementada.
* Página `/history` criada.
* Ordenação por data e ID implementada.
* Página de detalhes do upload criada.
* Tratamento 404 para upload inexistente implementado.

### Reprocessamento de uploads

* Rota de reprocessamento criada.
* Arquivo original localizado pelo caminho persistido.
* Planilha carregada novamente com Pandas.
* Metadados recalculados.
* Análise automática recalculada.
* Gráficos recalculados.
* Prévia reconstruída.
* Tratamento de arquivo físico ausente implementado.
* Tratamento de extensão não suportada implementado.

### Relatórios PDF

* Serviço `reports.py` criado.
* Geração de PDF com ReportLab implementada.
* Identificação do upload incluída no PDF.
* Nome do arquivo incluído.
* Extensão incluída.
* Quantidade de linhas incluída.
* Quantidade de colunas incluída.
* Data de criação incluída.
* Análise automática incluída.
* Colunas numéricas incluídas.
* Colunas categóricas incluídas.
* Valores ausentes incluídos.
* Estatísticas numéricas incluídas.
* Gráficos incluídos.
* Prévia limitada dos dados incluída.
* Pasta de relatórios criada automaticamente.
* Download do PDF implementado.

---

### Conversa 16 — Prévia dos dados no relatório PDF

* Parâmetro opcional `dataframe` adicionado ao gerador de relatórios.
* Prévia das primeiras linhas e colunas incluída no PDF.
* Limites de linhas e colunas implementados.
* Tratamento de DataFrame vazio implementado.
* Tabela adaptada ao tamanho da página.
* Testes de prévia adicionados.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `67 passed`.

---

### Conversa 17 — Persistência dos relatórios PDF

* Modelo `ReportRecord` criado.
* Relacionamento entre upload e relatório criado.
* Serviço `report_history.py` criado.
* Registro do relatório no banco implementado.
* Caminho físico do PDF persistido.
* Nome do relatório persistido.
* Data de geração persistida.
* Consulta por upload implementada.
* Página de detalhes passou a exibir relatórios relacionados.
* Download de relatório já existente implementado.
* Tratamento de relatório inexistente implementado.
* Tratamento de PDF físico ausente implementado.
* Testes de persistência adicionados.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `76 passed`.

---

### Conversa 18 — Histórico geral de relatórios

* Rota `/reports` criada.
* Página `reports_history.html` criada.
* Listagem geral de relatórios implementada.
* Upload de origem exibido.
* Link para detalhes do upload adicionado.
* Download do PDF existente adicionado.
* Estado vazio implementado.
* Link de navegação para relatórios adicionado.
* Carregamento antecipado com `joinedload()` implementado.
* Consultas adicionais desnecessárias evitadas.
* Testes da página geral adicionados.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `81 passed`.

---

### Conversa 19 — Exclusão segura de relatórios persistidos

* Função `delete_report_record()` criada.
* Exclusão de registros da tabela `report_records` implementada.
* Remoção do arquivo PDF físico implementada.
* Registro do banco passou a ser removido mesmo quando o arquivo físico já não existe.
* Retorno booleano criado para informar se o arquivo físico foi removido.
* Commit e rollback implementados no serviço de exclusão.
* Rota POST `/reports/<int:report_id>/delete` criada.
* Exclusões por requisição GET foram evitadas.
* Tratamento 404 implementado para relatórios inexistentes.
* Tratamento de falhas inesperadas com log da aplicação implementado.
* Mensagens de sucesso e erro adicionadas.
* Redirecionamento após exclusão implementado.
* Usuário pode retornar ao histórico geral de relatórios.
* Usuário pode retornar à página de detalhes do upload.
* Botão “Excluir” adicionado ao histórico geral de relatórios.
* Botão “Excluir” adicionado à lista de relatórios de cada upload.
* Confirmação JavaScript adicionada antes da exclusão.
* Campo oculto `redirect_to` criado para controlar o redirecionamento.
* Estilo visual de ação destrutiva adicionado ao `style.css`.
* Teste de exclusão do arquivo físico e registro criado.
* Teste de exclusão quando o arquivo físico não existe criado.
* Teste de exibição do formulário de exclusão criado.
* Teste da rota de exclusão criado.
* Teste de erro 404 criado.
* Teste do formulário na página de detalhes do upload criado.
* Teste do redirecionamento para os detalhes do upload criado.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `88 passed`.

---

### Conversa 20 — Exclusão segura de uploads e arquivos associados

* Estrutura `UploadDeletionResult` criada para representar o resultado da exclusão.
* Função `delete_upload_record()` criada no serviço de histórico.
* Função auxiliar `_delete_physical_file()` criada.
* Exclusão do arquivo CSV, XLSX ou XLS original implementada.
* Exclusão dos arquivos PDF relacionados ao upload implementada.
* Exclusão do registro do upload implementada.
* Exclusão em cascata dos registros de relatórios utilizada.
* Relacionamento `cascade="all, delete-orphan"` mantido no modelo.
* Exclusão completa realizada em uma única transação de banco.
* Commit e rollback implementados.
* Arquivos físicos ausentes passaram a ser tratados sem impedir a exclusão dos registros.
* Contagem de arquivos físicos ausentes implementada.
* Contagem de relatórios excluídos implementada.
* Preservação de uploads não relacionados validada.
* Rota POST `/history/<int:record_id>/delete` criada.
* Tratamento 404 implementado para uploads inexistentes.
* Tratamento de erros inesperados com log da aplicação implementado.
* Mensagens de sucesso adicionadas.
* Mensagem específica adicionada quando algum arquivo físico já não existe.
* Redirecionamento para o histórico de uploads implementado.
* Botão “Excluir upload” adicionado à página de detalhes.
* Botão “Excluir” adicionado ao histórico de uploads.
* Confirmação JavaScript adicionada antes da exclusão.
* Teste de exclusão do upload e de todos os arquivos relacionados criado.
* Teste de exclusão com arquivos físicos ausentes criado.
* Teste de preservação de outros uploads criado.
* Teste do formulário na página de detalhes criado.
* Teste do formulário no histórico de uploads criado.
* Teste da rota de exclusão completa criado.
* Teste de erro 404 criado.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `95 passed`.

---

## Arquivos modificados na Conversa 19

```text
app/services/report_history.py
app/routes.py
app/templates/reports_history.html
app/templates/upload_detail.html
app/static/css/style.css
tests/test_report_history.py
tests/test_history.py
PROJECT_STATE.md
```

---

## Arquivos modificados na Conversa 20

```text
app/services/history.py
app/routes.py
app/templates/upload_detail.html
app/templates/history.html
tests/test_history.py
PROJECT_STATE.md
```

---

## Arquivos analisados sem necessidade de alteração na Conversa 20

```text
app/models.py
app/services/report_history.py
app/static/css/style.css
tests/test_report_history.py
```

---

## Rotas atuais

### Página inicial

```text
GET /
```

### Upload

```text
GET /upload
POST /upload
```

### Dashboard

```text
GET /dashboard
```

### Histórico de uploads

```text
GET /history
```

### Detalhes do upload

```text
GET /history/<record_id>
```

### Reprocessamento

```text
GET /history/<record_id>/reprocess
```

### Geração de relatório

```text
GET /history/<record_id>/report
```

### Exclusão do upload

```text
POST /history/<record_id>/delete
```

### Histórico geral de relatórios

```text
GET /reports
```

### Download de relatório existente

```text
GET /reports/<report_id>/download
```

### Exclusão de relatório

```text
POST /reports/<report_id>/delete
```

---

## Estado funcional atual

O DataBoard Reports atualmente permite:

* enviar arquivos CSV, XLSX e XLS;
* validar os tipos de arquivos permitidos;
* salvar os arquivos enviados no servidor;
* carregar planilhas com Pandas;
* extrair metadados da planilha;
* exibir uma prévia dos dados;
* identificar colunas numéricas e categóricas;
* calcular valores ausentes e percentuais;
* gerar estatísticas numéricas;
* gerar gráficos automáticos com Plotly;
* registrar uploads em banco SQLite;
* consultar o histórico de uploads;
* visualizar os detalhes de cada upload;
* reprocessar arquivos já enviados;
* gerar relatórios PDF com ReportLab;
* incluir análise, estatísticas, gráficos e prévia no PDF;
* persistir os relatórios gerados;
* listar relatórios por upload;
* consultar o histórico geral de relatórios;
* baixar novamente relatórios existentes;
* excluir relatórios individualmente;
* remover o arquivo PDF ao excluir um relatório;
* excluir uploads completos;
* remover o arquivo original da planilha;
* remover os PDFs relacionados ao upload;
* excluir registros de relatórios em cascata;
* tratar arquivos físicos ausentes durante a exclusão;
* preservar registros e arquivos não relacionados;
* executar ações destrutivas somente por requisições `POST`;
* validar o comportamento da aplicação com 95 testes automatizados.

---

## Resultado atual dos testes

Comando executado:

```bash
python -m pytest
```

Resultado validado na Conversa 20:

```text
95 passed in 29.61s
```

---

## Cobertura funcional dos testes

Os testes atuais validam:

* arquivos permitidos;
* arquivos não permitidos;
* leitura de CSV;
* leitura de XLSX;
* leitura de XLS;
* arquivo inexistente;
* metadados da planilha;
* análise de colunas numéricas;
* análise de colunas categóricas;
* valores ausentes;
* estatísticas numéricas;
* gráficos automáticos;
* upload de arquivo;
* registro no banco;
* histórico de uploads;
* detalhes do upload;
* reprocessamento;
* arquivo físico ausente;
* geração de PDF;
* conteúdo básico do PDF;
* gráficos no PDF;
* prévia no PDF;
* persistência dos relatórios;
* relacionamento entre upload e relatório;
* histórico geral de relatórios;
* download de relatório existente;
* exclusão individual de relatório;
* exclusão de upload;
* exclusão em cascata dos relatórios;
* remoção dos arquivos físicos;
* tratamento de arquivos físicos ausentes;
* preservação de registros não relacionados;
* respostas 404;
* formulários de exclusão;
* redirecionamentos após exclusão.

---

## Decisões técnicas atuais

* Flask continua sendo utilizado como framework web.
* Pandas continua responsável pela leitura e análise das planilhas.
* Plotly continua responsável pelos gráficos interativos.
* ReportLab continua responsável pelos relatórios PDF.
* SQLite continua sendo utilizado durante o desenvolvimento.
* SQLAlchemy continua sendo utilizado como ORM.
* A application factory continua sendo utilizada.
* As regras de negócio continuam concentradas em serviços.
* As rotas permanecem responsáveis pela coordenação das requisições.
* Os templates continuam utilizando Jinja.
* As ações destrutivas utilizam requisições `POST`.
* Os arquivos físicos e os registros do banco são tratados separadamente.
* A exclusão de upload utiliza uma única transação de banco.
* O relacionamento em cascata remove os relatórios associados.
* Os testes utilizam banco SQLite em memória.
* Cada nova entrega deve manter todos os testes anteriores funcionando.

---

## Regras de continuidade

Nas próximas conversas:

* realizar alterações pequenas e sequenciais;
* evitar mudanças fora do escopo da entrega;
* manter compatibilidade com as funcionalidades existentes;
* criar testes para cada novo comportamento;
* executar testes específicos antes da suíte completa;
* atualizar o `PROJECT_STATE.md` após cada entrega;
* criar um commit separado para cada conversa;
* não iniciar uma nova funcionalidade antes de todos os testes passarem;
* manter as rotas destrutivas utilizando `POST`;
* manter commit e rollback nas operações de persistência;
* preservar a separação entre rotas, serviços, modelos e templates.

---

## O que ainda não foi implementado

* Persistência completa da análise automática.
* Persistência dos gráficos gerados.
* Persistência da prévia da planilha.
* Confirmação de exclusão sem JavaScript inline.
* Proteção CSRF nos formulários.
* Exclusão em massa.
* Lixeira e restauração de uploads e relatórios.
* Autenticação.
* Permissões por usuário.
* Filtros no histórico.
* Busca no histórico.
* Paginação.
* Ordenação configurável.
* Dashboards customizáveis.
* Upload múltiplo.
* Exportação para outros formatos.
* API REST.
* Migrações com Flask-Migrate.
* Pipeline CI/CD.
* Dockerização concluída.
* Deploy.
* Monitoramento.
* Logs estruturados.
* Backup automático.
* Banco PostgreSQL em produção.

---

## Próxima entrega sugerida

Conversa 21 — Paginação e busca no histórico de uploads e relatórios

## Objetivo provável da Conversa 21

Melhorar a navegação dos históricos, permitindo localizar uploads e relatórios com facilidade quando houver grande quantidade de registros.

---

## Escopo recomendado para a Conversa 21

* Adicionar campo de busca no histórico de uploads.
* Permitir busca pelo nome do arquivo.
* Adicionar paginação ao histórico de uploads.
* Adicionar busca ao histórico de relatórios.
* Permitir busca pelo nome do relatório.
* Permitir busca pelo nome do upload de origem.
* Adicionar paginação ao histórico de relatórios.
* Preservar a busca ao navegar entre páginas.
* Exibir quantidade total de resultados.
* Exibir página atual.
* Exibir total de páginas.
* Exibir estado vazio para buscas sem resultado.
* Organizar as consultas na camada de serviços.
* Manter compatibilidade com SQLite.
* Criar testes unitários dos serviços.
* Criar testes de integração das rotas.
* Manter os 95 testes anteriores funcionando.

---

## Manter fora do escopo da Conversa 21

* Filtros avançados por data.
* Ordenação configurável pelo usuário.
* Exclusão em massa.
* Autenticação.
* Permissões.
* Proteção CSRF.
* Flask-Migrate.
* Docker.
* Deploy.

---

## Critérios de conclusão da Conversa 21

A Conversa 21 deverá ser considerada concluída quando:

* a busca de uploads funcionar;
* a busca de relatórios funcionar;
* a paginação de uploads funcionar;
* a paginação de relatórios funcionar;
* os filtros forem preservados entre páginas;
* estados vazios forem exibidos corretamente;
* registros não relacionados não forem afetados;
* os novos testes forem aprovados;
* todos os testes anteriores continuarem passando;
* o `PROJECT_STATE.md` for atualizado;
* o commit da entrega for criado.

---

## Observação de continuidade

A Conversa 20 concluiu o ciclo completo de exclusão dos dados persistidos.

O projeto agora permite:

1. enviar e processar planilhas;
2. analisar automaticamente os dados;
3. gerar gráficos interativos;
4. registrar e reprocessar uploads;
5. gerar relatórios PDF completos;
6. persistir e consultar relatórios;
7. baixar novamente PDFs existentes;
8. excluir relatórios individualmente;
9. excluir uploads e todos os arquivos relacionados;
10. tratar arquivos físicos ausentes;
11. preservar dados não relacionados;
12. validar o comportamento com 95 testes automatizados.

A partir da Conversa 21, o projeto deverá evoluir para busca e paginação dos históricos, preparando a aplicação para uma quantidade maior de uploads e relatórios.
````
