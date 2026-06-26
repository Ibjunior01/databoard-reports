# PROJECT_STATE.md

## Projeto

DataBoard Reports

## Repositório local sugerido

spreadsheet-dashboard-platform

## Repositório sugerido no GitHub

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

## Entrega atual

Conversa 2 — Upload inicial de arquivos CSV e Excel

## Checklist de Entregas

### 01 — Base inicial Flask

Status: OK

O que foi concluído:

* Estrutura inicial de pastas criada.
* Aplicação Flask criada.
* Application factory criada.
* Página inicial criada.
* Template base criado.
* CSS inicial criado.
* Arquivo de configuração centralizado criado.
* requirements.txt criado.
* .gitignore criado.
* .env.example criado.
* Dockerfile inicial criado.
* docker-compose.yml inicial criado.
* README.md inicial criado.
* PROJECT_STATE.md criado.
* Arquivos placeholder da camada de services criados.
* Pastas uploads, reports e sample_data criadas.
* Arquivo conftest.py criado para corrigir importações no Pytest.
* Testes iniciais criados.
* Servidor Flask rodando em http://127.0.0.1:5000.
* Pytest executado com sucesso.
* Resultado dos testes: 3 passed.

### 02 — Upload inicial de arquivos CSV e Excel

Status: Próximo

Objetivo:

* Criar rota GET /upload.
* Criar rota POST /upload.
* Ativar o link Upload no menu.
* Criar tela de upload.
* Criar formulário HTML com enctype="multipart/form-data".
* Permitir somente arquivos .csv, .xlsx e .xls.
* Validar extensão do arquivo antes de salvar.
* Usar secure_filename do Werkzeug para tratar o nome do arquivo.
* Salvar arquivos enviados em app/uploads.
* Exibir mensagens de sucesso e erro usando flash messages do Flask.
* Criar testes para validação de extensão.
* Criar teste para rota GET /upload.
* Atualizar README.md.
* Atualizar PROJECT_STATE.md ao final da conversa.

### 03 — Leitura inicial de arquivos com Pandas

Status: Em breve

Objetivo previsto:

* Ler arquivos CSV.
* Ler arquivos Excel.
* Criar funções em app/services/data_loader.py.
* Validar se o arquivo possui dados.
* Exibir uma prévia simples da planilha.
* Criar testes para leitura de CSV e Excel.

### 04 — Análise automática inicial

Status: Em breve

Objetivo previsto:

* Identificar colunas numéricas.
* Identificar colunas categóricas.
* Calcular total de linhas.
* Calcular total de colunas.
* Gerar indicadores simples.
* Preparar os dados para o futuro dashboard.

### 05 — Dashboard inicial

Status: Em breve

Objetivo previsto:

* Criar rota /dashboard.
* Exibir indicadores básicos.
* Criar primeiros gráficos com Plotly.
* Organizar visualmente os dados processados.

### 06 — Histórico de uploads

Status: Em breve

Objetivo previsto:

* Implementar SQLite.
* Criar modelos com SQLAlchemy.
* Registrar arquivos enviados.
* Exibir histórico em /history.

### 07 — Exportação de relatório PDF

Status: Em breve

Objetivo previsto:

* Gerar relatórios em PDF com ReportLab.
* Exportar resumo da análise.
* Salvar relatórios em app/reports.
* Criar botão de download.

### 08 — Docker, documentação e portfólio

Status: Em breve

Objetivo previsto:

* Revisar Dockerfile.
* Revisar docker-compose.yml.
* Melhorar README.md.
* Adicionar prints do projeto.
* Preparar o repositório para GitHub.
* Preparar conteúdo para divulgação no LinkedIn.

## O que foi implementado na Conversa 1

* Estrutura inicial de pastas.
* Application factory do Flask.
* Página inicial.
* Template base.
* CSS inicial.
* Arquivo de configuração centralizado.
* Arquivo requirements.txt.
* Arquivo .gitignore.
* Arquivo .env.example.
* Dockerfile inicial.
* docker-compose.yml inicial.
* README.md inicial.
* PROJECT_STATE.md inicial.
* Arquivos placeholder para futuras camadas de serviço.
* Testes mínimos de importação para os módulos de serviço.
* Teste básico da rota inicial.
* Arquivo conftest.py para corrigir importações no Pytest.
* Pastas uploads, reports e sample_data versionadas com .gitkeep.

## Status técnico validado na Conversa 1

A aplicação foi executada com sucesso usando:

```bash
python run.py
```

A aplicação abriu corretamente em:

```text
http://127.0.0.1:5000
```

Os testes foram executados com sucesso usando:

```bash
python -m pytest
```

Resultado final:

```text
3 passed
```

## Funcionalidades ainda não implementadas

* Upload de arquivos.
* Leitura de CSV.
* Leitura de Excel.
* Validação real de planilhas.
* Banco de dados.
* Modelos SQLAlchemy.
* Gráficos com Plotly.
* Dashboard dinâmico.
* Histórico de arquivos processados.
* Exportação de relatórios em PDF.
* Autenticação.
* Deploy em nuvem.
* Pipeline CI/CD.

## Arquitetura atual

A aplicação usa o padrão application factory do Flask.

Arquivo principal:

* run.py

Pacote principal:

* app/

Arquivos centrais:

* app/**init**.py
* app/config.py
* app/routes.py
* app/models.py

Templates:

* app/templates/base.html
* app/templates/index.html
* app/templates/upload.html
* app/templates/dashboard.html
* app/templates/history.html

Arquivos estáticos:

* app/static/css/style.css

Camada de serviços preparada:

* app/services/data_loader.py
* app/services/analyzer.py
* app/services/charts.py
* app/services/reports.py

Pastas preparadas para arquivos futuros:

* app/uploads/
* app/reports/
* sample_data/

Testes atuais:

* tests/test_analyzer.py
* tests/test_data_loader.py
* tests/test_routes.py

Arquivo auxiliar de testes:

* conftest.py

## Rotas existentes

### GET /

Renderiza a página inicial da aplicação.

Função responsável:

* index()

Arquivo:

* app/routes.py

## Decisões técnicas tomadas

* O projeto usará Flask com application factory para facilitar testes, organização e evolução.
* A configuração foi centralizada em app/config.py.
* As funcionalidades futuras foram separadas em uma camada de services.
* Uploads e relatórios gerados terão pastas próprias.
* Banco de dados ainda não foi implementado para manter a primeira entrega simples.
* Os templates de upload, dashboard e histórico foram criados inicialmente como placeholders.
* O menu exibe funcionalidades futuras como itens desabilitados.
* Bootstrap foi usado via CDN para acelerar a criação visual inicial.
* CSS customizado foi criado em app/static/css/style.css.
* Dockerfile e docker-compose.yml foram adicionados de forma inicial, sem configurações avançadas.
* conftest.py foi adicionado para garantir que o Pytest consiga importar o pacote app.
* Os testes iniciais validam a importação dos serviços e a rota principal.

## Como rodar localmente

Criar ambiente virtual:

```bash
python -m venv venv
```

Ativar no Windows:

```bash
venv\Scripts\activate
```

Ativar no Linux/macOS:

```bash
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Rodar aplicação:

```bash
python run.py
```

Acessar no navegador:

```text
http://127.0.0.1:5000
```

## Como rodar com Docker

```bash
docker compose up --build
```

Acessar no navegador:

```text
http://127.0.0.1:5000
```

## Como rodar testes

Com o ambiente virtual ativado:

```bash
python -m pytest
```

Resultado atual esperado:

```text
3 passed
```

## Estrutura atual do projeto

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
│   └── test_routes.py
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

## Objetivo da Conversa 2

Implementar a funcionalidade inicial de upload de arquivos CSV e Excel.

## Escopo da Conversa 2

Nesta entrega, implementar:

* Rota GET /upload.
* Rota POST /upload.
* Link Upload ativo no menu do base.html.
* Tela profissional de upload em upload.html.
* Formulário HTML com enctype="multipart/form-data".
* Validação de extensão para .csv, .xlsx e .xls.
* Uso de secure_filename do Werkzeug.
* Salvamento dos arquivos dentro de app/uploads.
* Flash messages para sucesso e erro.
* CSS complementar para a tela de upload, se necessário.
* Testes básicos para validação de extensão.
* Teste básico para verificar se GET /upload retorna status 200.
* Atualização do README.md.
* Atualização deste PROJECT_STATE.md ao final da conversa.

## Regras da Conversa 2

* Não implementar leitura dos dados com Pandas ainda.
* Não implementar dashboard ainda.
* Não implementar gráficos ainda.
* Não implementar banco de dados ainda.
* Não implementar SQLAlchemy ainda.
* Não implementar histórico ainda.
* Não implementar geração de PDF ainda.
* Não implementar autenticação ainda.
* Não aumentar o escopo da entrega.
* Manter o código simples, limpo e profissional.

## Arquivos que provavelmente serão alterados na Conversa 2

* app/routes.py
* app/templates/base.html
* app/templates/upload.html
* app/static/css/style.css
* tests/test_routes.py
* README.md
* PROJECT_STATE.md

## Arquivos que talvez sejam criados na Conversa 2

* tests/test_upload.py

## Resultado esperado no navegador para a Conversa 2

Ao acessar:

```text
http://127.0.0.1:5000/upload
```

Deve aparecer uma página de upload.

Ao enviar um arquivo válido, como:

* .csv
* .xlsx
* .xls

O sistema deve salvar o arquivo em:

```text
app/uploads/
```

E mostrar uma mensagem de sucesso.

Ao enviar um arquivo inválido, como:

* .txt
* .pdf
* .png

O sistema não deve salvar o arquivo e deve mostrar uma mensagem de erro.

## Resultado esperado nos testes após a Conversa 2

Ao rodar:

```bash
python -m pytest
```

Todos os testes devem passar.

## Commit da Conversa 1

Commit sugerido ou realizado:

```bash
git commit -m "chore: create initial Flask project structure"
```

## Commit sugerido para a Conversa 2

```bash
git commit -m "feat: add spreadsheet upload page"
```

## Prompt recomendado para iniciar a Conversa 2

Vamos iniciar a Conversa 2 do projeto DataBoard Reports.

Use como base o PROJECT_STATE.md atualizado.

Agora quero implementar apenas a funcionalidade inicial de upload de arquivos CSV e Excel.

Regras:

* Não implemente leitura dos dados com Pandas ainda.
* Não implemente dashboard ainda.
* Não implemente banco de dados ainda.
* Não implemente gráficos ainda.
* Não implemente relatório PDF ainda.
* Mantenha a entrega pequena e profissional.
* Crie rota GET /upload.
* Crie rota POST /upload.
* Ative o link Upload no menu.
* Crie formulário HTML para upload.
* Valide extensões permitidas: .csv, .xlsx e .xls.
* Use secure_filename do Werkzeug.
* Salve arquivos em app/uploads.
* Mostre mensagens de sucesso e erro usando flash messages do Flask.
* Crie testes básicos para validação de extensão.
* Crie teste para GET /upload retornar status 200.
* Atualize o README.md.
* Atualize o PROJECT_STATE.md ao final.

Entregue os arquivos completos e explique onde cada um deve ficar.
