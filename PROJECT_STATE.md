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
* Flask-SQLAlchemy
* ReportLab
* HTML/CSS
* Bootstrap
* Docker
* Pytest
* Git/GitHub

## Identidade visual definida

O projeto segue uma identidade visual dark/profissional, inspirada em dashboards SaaS modernos.

### Direção visual

* Fundo principal em azul muito escuro/preto técnico.
* Cards em tons de slate/navy.
* Azul claro como cor primária de ação.
* Bordas discretas.
* Sombras suaves para profundidade.
* Layout limpo, moderno e profissional.
* Foco em visual de produto SaaS para portfólio.

---

## Entrega atual

Conversa 12 — Geração inicial de relatório PDF

## Objetivo da entrega atual

Criar a primeira funcionalidade de exportação em PDF do DataBoard Reports, permitindo gerar e baixar um relatório básico contendo os principais metadados de um upload registrado.

Essa entrega aproxima o sistema de seu objetivo principal: transformar planilhas processadas em relatórios que possam ser armazenados, compartilhados e apresentados.

---

## O que já foi implementado

### Conversa 01 — Base inicial Flask

* Estrutura inicial de pastas criada.
* Application factory do Flask implementada.
* Página inicial criada.
* Template base criado.
* CSS inicial configurado.
* Arquivo de configuração centralizado criado.
* Arquivo `requirements.txt` criado.
* Arquivo `run.py` criado.
* Testes iniciais de rotas criados.

### Conversa 02 — Upload de arquivos CSV/Excel

* Tela de upload criada.
* Rota GET `/upload` criada.
* Rota POST `/upload` criada.
* Upload de arquivos `.csv`, `.xlsx` e `.xls` implementado.
* Validação de extensões permitidas implementada.
* Bloqueio de arquivos inválidos criado.
* Salvamento seguro de arquivos com `secure_filename`.
* Pasta `app/uploads/` preparada.
* Testes de upload criados.

### Conversa 03 — Leitura de arquivos CSV/Excel

* Serviço `data_loader.py` criado.
* Leitura de arquivos CSV implementada com Pandas.
* Leitura de arquivos Excel implementada com Pandas.
* Extração de metadados básicos implementada.
* Contagem de linhas e colunas implementada.
* Tratamento para tipo de arquivo não suportado criado.
* Testes para leitura de CSV e Excel criados.

### Conversa 04 — Exibição prévia dos dados

* Template `dashboard.html` criado.
* Fluxo pós-upload passou a renderizar dashboard.
* Exibição de metadados da planilha implementada.
* Exibição de prévia dos dados implementada.
* Visual do dashboard alinhado à identidade dark/profissional.
* Testes de integração com upload e dashboard ajustados.

### Conversa 05 — Análise automática dos dados

* Serviço `analyzer.py` criado.
* Identificação de colunas numéricas implementada.
* Identificação de colunas categóricas/texto implementada.
* Cálculo de valores ausentes por coluna implementado.
* Cálculo de percentual de valores ausentes implementado.
* Estatísticas básicas de colunas numéricas implementadas.
* Resultado da análise automática integrado ao dashboard.
* Testes do analisador criados.

### Conversa 06 — Exibição da análise automática

* Dashboard atualizado para exibir análise automática.
* Cards de resumo adicionados.
* Seção de colunas numéricas criada.
* Seção de colunas categóricas/texto criada.
* Seção de qualidade dos dados criada.
* Exibição de estatísticas básicas adicionada.
* Layout visual refinado.

### Conversa 07 — Gráficos automáticos com Plotly

* Serviço `charts.py` criado.
* Geração automática de gráfico de barras para coluna categórica/texto implementada.
* Geração automática de histograma para coluna numérica implementada.
* Gráficos Plotly integrados ao dashboard.
* Visual dos gráficos alinhado ao tema dark/profissional.
* Estado vazio criado para quando não houver colunas compatíveis.
* Testes de gráficos criados.

### Conversa 08 — Histórico inicial de uploads com SQLite e SQLAlchemy

* Arquivo `requirements.txt` atualizado com a dependência `Flask-SQLAlchemy`.

* Arquivo `app/extensions.py` criado.

* Instância global `db = SQLAlchemy()` criada para centralizar as extensões do Flask.

* Arquivo `app/config.py` atualizado com configurações de banco de dados.

* Configuração `SQLALCHEMY_DATABASE_URI` adicionada usando SQLite local.

* Configuração `SQLALCHEMY_TRACK_MODIFICATIONS = False` adicionada.

* Arquivo `app/__init__.py` atualizado.

* Inicialização do banco integrada à application factory.

* Criação automática das tabelas com `db.create_all()` adicionada ao contexto da aplicação.

* Blueprint corrigida para uso de `main_bp`.

* Arquivo `app/models.py` atualizado.

* Modelo `UploadRecord` criado.

* Tabela `upload_records` criada.

* Campos iniciais do histórico definidos:

  * `id`;
  * `file_name`;
  * `file_extension`;
  * `row_count`;
  * `column_count`;
  * `created_at`.

* Arquivo `app/services/history.py` criado.

* Função `create_upload_record()` criada para salvar registros de upload.

* Função `list_upload_records()` criada para listar registros recentes.

* Tratamento de commit e rollback implementado no serviço de histórico.

* Rota POST `/upload` integrada ao histórico.

* Cada upload válido agora salva um registro no banco de dados.

* Rota GET `/history` criada.

* Template `history.html` criado.

* Página de histórico passou a listar uploads anteriores.

* Link “Histórico” ativado no menu principal.

* Estilos da tabela de histórico adicionados ao `style.css`.

* Arquivo `conftest.py` atualizado para usar banco SQLite em memória durante os testes.

* Arquivo `tests/test_history.py` criado.

* Teste para criação de registro de upload criado.

* Teste para listagem dos registros mais recentes criado.

* Teste de acesso à página `/history` criado.

* Teste de integração validando que um upload cria registro no histórico criado.

* Arquivo `.gitignore` atualizado para ignorar banco local e pasta `instance/`.

* O comando `python -m pytest` retornou `32 passed`.

### Conversa 09 — Página de detalhes do upload

* Rota GET `/history/<int:record_id>` criada.

* Busca individual de registro de upload pelo ID implementada.

* Função `get_upload_record()` criada no serviço de histórico.

* Tratamento de erro 404 implementado para uploads inexistentes.

* Template `upload_detail.html` criado.

* Página individual de detalhes do upload criada.

* Link “Ver detalhes” adicionado à tabela da página `/history`.

* Página de detalhes passou a exibir:

  * ID;
  * nome do arquivo;
  * extensão;
  * quantidade de linhas;
  * quantidade de colunas;
  * data/hora de criação.

* Botão para voltar ao histórico criado.

* Estilos da página de detalhes adicionados ao `style.css`.

* Teste de acesso à página de detalhes criado.

* Teste para registro inexistente retornar 404 criado.

* Teste validando link de detalhes na página `/history` criado.

* O comando `python -m pytest` retornou `35 passed`.

### Conversa 10 — Persistência do caminho do arquivo enviado

* Campo `file_path` adicionado ao modelo `UploadRecord`.
* Caminho físico do arquivo enviado passou a ser salvo no banco de dados.
* Função `create_upload_record()` atualizada para receber `file_path`.
* Rota POST `/upload` atualizada para persistir o caminho do arquivo salvo.
* Página de detalhes do upload passou a exibir o caminho salvo do arquivo.
* Teste de criação de registro atualizado para validar `file_path`.
* Teste de upload atualizado para validar que o caminho do arquivo foi salvo.
* Teste de detalhes atualizado para validar a exibição do caminho do arquivo.
* Teste específico criado para validar a persistência de `file_path`.
* Fixture duplicado de `client` removido de `tests/test_routes.py`.
* Testes passaram a usar corretamente o `client` global configurado em `conftest.py`.
* Banco SQLite em memória passou a ser usado corretamente nos testes de rotas.
* O comando `python -m pytest` retornou `36 passed`.

### Conversa 11 — Reprocessamento de uploads antigos

* Botão “Reprocessar upload” adicionado à página de detalhes do upload.
* Rota GET `/history/<int:record_id>/reprocess` criada.
* Busca individual do registro de upload reutilizada para reprocessamento.
* Tratamento 404 implementado para tentativa de reprocessar upload inexistente.
* Validação de existência física do arquivo salvo em `file_path` implementada.
* Mensagem de erro exibida quando o arquivo físico não é encontrado no servidor.
* Reprocessamento de planilha antiga implementado usando o caminho salvo.
* Metadados recalculados a partir do arquivo antigo.
* Análise automática recalculada a partir do arquivo antigo.
* Prévia dos dados recriada a partir do arquivo antigo.
* Gráficos automáticos regenerados a partir do arquivo antigo.
* Dashboard renderizado novamente a partir de um upload histórico.
* Teste criado para validar botão de reprocessamento na página de detalhes.
* Teste criado para validar erro 404 em upload inexistente.
* Teste criado para validar mensagem de erro quando o arquivo físico não existe.
* Teste criado para validar reprocessamento com sucesso.
* O comando `python -m pytest` retornou `40 passed`.


### Conversa 12 — Geração inicial de relatório PDF

* Dependência `ReportLab` adicionada ao projeto.
* Serviço `app/services/reports.py` criado.
* Função `generate_upload_report()` implementada.
* Geração física de arquivos PDF implementada.
* Criação automática da pasta de relatórios implementada.
* Nome seguro e único para cada relatório implementado.
* Nome do relatório passou a incluir:
  * ID do upload;
  * nome seguro do arquivo;
  * data e hora de geração.
* Relatório inicial passou a exibir:
  * título do sistema;
  * descrição do relatório;
  * ID do upload;
  * nome do arquivo;
  * extensão;
  * quantidade de linhas;
  * quantidade de colunas;
  * data do upload;
  * data de geração do relatório.
* Formatação de data e hora implementada.
* Layout inicial do relatório criado com tabela estilizada.
* Identidade visual do PDF alinhada ao projeto.
* Tratamento para nomes de arquivos longos implementado.
* Quebra automática do nome do arquivo em múltiplas linhas adicionada.
* Escape de caracteres especiais em nomes de arquivos implementado.
* Rota GET `/history/<int:record_id>/report` criada.
* Busca do registro pelo ID integrada à geração do PDF.
* Tratamento 404 para tentativa de gerar relatório de registro inexistente implementado.
* Download do PDF implementado com `send_file()`.
* Cabeçalho `Content-Disposition` configurado para download como anexo.
* Arquivo PDF passou a ser salvo em `app/reports/`.
* Botão “Gerar PDF” adicionado à página de detalhes do upload.
* Testes unitários do serviço de relatórios criados.
* Teste de criação física do PDF criado.
* Teste de validação do cabeçalho `%PDF` criado.
* Teste de criação automática da pasta de relatórios criado.
* Teste de exibição do botão “Gerar PDF” criado.
* Teste da rota de download do relatório criado.
* Teste de erro 404 para relatório de registro inexistente criado.
* Arquivo `.gitignore` atualizado para ignorar PDFs gerados.
* Todos os testes automatizados permaneceram passando.
  
---

## Estrutura atual esperada

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

---

## Arquivos modificados na Conversa 08

```text
requirements.txt
app/__init__.py
app/config.py
app/extensions.py
app/models.py
app/routes.py
app/services/history.py
app/templates/base.html
app/templates/history.html
app/static/css/style.css
conftest.py
tests/test_history.py
.gitignore
PROJECT_STATE.md
```

## Arquivos modificados na Conversa 09

```text
app/services/history.py
app/routes.py
app/templates/history.html
app/templates/upload_detail.html
app/static/css/style.css
tests/test_history.py
PROJECT_STATE.md
```

## Arquivos modificados na Conversa 10

```text
app/models.py
app/services/history.py
app/routes.py
app/templates/upload_detail.html
tests/test_history.py
tests/test_routes.py
PROJECT_STATE.md
```

## Arquivos modificados na Conversa 11

```text
app/routes.py
app/templates/upload_detail.html
app/templates/base.html
app/static/css/style.css
tests/test_history.py
PROJECT_STATE.md
```

## Arquivos modificados na Conversa 12

```text
requirements.txt
app/services/reports.py
app/routes.py
app/templates/upload_detail.html
app/static/css/style.css
tests/test_reports.py
tests/test_history.py
.gitignore
PROJECT_STATE.md

---

## Resultado esperado dos testes

Use o número exibido no seu terminal. Caso tenham sido adicionados exatamente os seis testes planejados nesta conversa, o bloco deverá ficar assim:

```bash
python -m pytest
```

Resultado validado na Conversa 11:

```text
46 passed
```

---

## Estado funcional atual

Atualmente o sistema permite:

* acessar a página inicial;
* acessar a tela de upload;
* enviar arquivos `.csv`, `.xlsx` e `.xls`;
* bloquear arquivos com extensões inválidas;
* salvar o arquivo enviado com nome seguro;
* carregar a planilha com Pandas;
* extrair metadados básicos da planilha;
* exibir a prévia dos dados no dashboard;
* analisar automaticamente o DataFrame enviado;
* identificar colunas numéricas;
* identificar colunas categóricas/texto;
* calcular valores ausentes por coluna;
* calcular percentual de valores ausentes por coluna;
* calcular estatísticas básicas das colunas numéricas;
* exibir toda a análise automática no dashboard web;
* gerar gráficos automáticos com Plotly;
* gerar gráfico de barras para coluna categórica/texto;
* gerar histograma para coluna numérica;
* exibir os gráficos automáticos no dashboard;
* exibir estado vazio quando não houver colunas compatíveis para gráficos;
* manter o visual dos gráficos alinhado à identidade dark/profissional do projeto;
* registrar cada upload válido no banco SQLite;
* salvar nome do arquivo, extensão, quantidade de linhas, quantidade de colunas, data/hora e caminho salvo do arquivo;
* acessar a página `/history`;
* visualizar o histórico básico de uploads em tabela;
* clicar em “Ver detalhes” em um upload registrado;
* acessar a página individual `/history/<id>`;
* visualizar os metadados individuais de um upload;
* visualizar o caminho salvo do arquivo na página de detalhes;
* receber erro 404 ao tentar acessar detalhes de upload inexistente;
* clicar em “Reprocessar upload” na página de detalhes;
* reprocessar um arquivo antigo usando o caminho salvo em `file_path`;
* recarregar a planilha antiga sem precisar fazer novo upload;
* recalcular metadados, análise automática e gráficos de um upload antigo;
* receber mensagem amigável quando o arquivo físico de um upload antigo não existe mais;
* usar banco SQLite em memória nos testes automatizados;
* validar o comportamento com 40 testes automatizados.
* gerar um relatório PDF básico a partir de um upload registrado;
* salvar relatórios gerados na pasta `app/reports/`;
* baixar o relatório PDF pelo navegador;
* gerar nomes seguros e únicos para os relatórios;
* exibir no PDF os principais metadados do upload;
* formatar datas e horários no relatório;
* quebrar nomes longos de arquivos em múltiplas linhas;
* receber erro 404 ao solicitar relatório de upload inexistente;
* acessar a geração de PDF pela página de detalhes do upload.
---

## O que ainda não foi implementado

* Persistência da análise automática completa.
* Persistência dos gráficos gerados.
* Persistência da prévia da planilha.
* Relatórios PDF avançados com análise automática.
* Inserção de gráficos no PDF.
* Inserção de prévia da planilha no PDF.
* Persistência dos relatórios gerados no banco de dados.
* Histórico de relatórios gerados.
* Autenticação.
* Deploy.
* Pipeline CI/CD.
* Filtros avançados.
* Dashboards customizáveis.
* Upload múltiplo.
* Exclusão de registros de histórico.
* Edição de registros de histórico.
* Migrações profissionais de banco com Flask-Migrate.
* Permissões por usuário.

---

## Próxima entrega sugerida

Conversa 13 — Inclusão da análise automática no relatório PDF

## Objetivo provável da Conversa 13

Evoluir o relatório PDF básico para apresentar também um resumo da análise automática da planilha, reutilizando o arquivo salvo no servidor e os serviços já existentes de carregamento e análise.

## Escopo recomendado para a Conversa 13

* Localizar o arquivo original pelo campo `file_path`.
* Recarregar a planilha com o serviço `data_loader.py`.
* Reutilizar o serviço `analyzer.py`.
* Inserir no PDF:
  * quantidade de colunas numéricas;
  * quantidade de colunas categóricas;
  * quantidade total de valores ausentes;
  * nomes das colunas numéricas;
  * nomes das colunas categóricas.
* Criar tratamento para arquivo físico inexistente.
* Criar testes para o relatório com análise automática.
* Manter gráficos e prévia da tabela fora desta entrega.

---

## Escopo recomendado para a Conversa 12

* Confirmar ou criar o serviço `reports.py`.
* Implementar geração inicial de PDF com ReportLab.
* Criar função para gerar relatório básico a partir de metadados do upload.
* Criar rota inicial para exportação de relatório.
* Adicionar botão “Gerar PDF” no dashboard ou na página de detalhes.
* Salvar o PDF gerado na pasta `app/reports/`.
* Retornar o arquivo PDF para download.
* Criar teste para geração do PDF.
* Criar teste para rota de exportação.

---

## Escopo recomendado inicial para geração de PDF

Para manter a entrega pequena, iniciar apenas com um relatório simples contendo:

* título do relatório;
* nome do arquivo;
* extensão;
* quantidade de linhas;
* quantidade de colunas;
* data/hora de geração do PDF.

A primeira versão do PDF não precisa conter gráficos, preview da tabela ou análise automática completa.

---

## Manter fora do escopo da Conversa 12

* Inserir gráficos Plotly no PDF.
* Inserir prévia da planilha no PDF.
* Inserir análise automática completa no PDF.
* Persistir relatório PDF no banco de dados.
* Criar histórico de relatórios gerados.
* Criar templates avançados de PDF.
* Criar layout corporativo completo.
* Criar autenticação.
* Criar permissões por usuário.
* Criar filtros avançados.
* Criar dashboards customizáveis.
* Criar upload múltiplo.
* Criar Flask-Migrate.
* Criar deploy.

---

## Observação de continuidade

A Conversa 11 concluiu o reprocessamento de uploads antigos.

O projeto agora possui um fluxo funcional para:

1. receber uma planilha;
2. salvar o arquivo no servidor;
3. carregar os dados com Pandas;
4. extrair metadados;
5. analisar a estrutura dos dados;
6. gerar gráficos automáticos;
7. exibir o dashboard;
8. registrar o upload no banco SQLite;
9. salvar o caminho do arquivo enviado;
10. listar uploads anteriores na página de histórico;
11. abrir uma página individual de detalhes para cada upload;
12. visualizar o caminho salvo do arquivo;
13. reprocessar um upload antigo usando o `file_path` salvo no banco;
14. recriar dashboard, metadados, análise automática e gráficos a partir de um arquivo antigo;
15. validar o comportamento com 40 testes automatizados.

A partir da Conversa 12, o projeto deve evoluir para a geração inicial de relatórios em PDF.
