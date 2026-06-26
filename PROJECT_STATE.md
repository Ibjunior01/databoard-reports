# PROJECT_STATE.md

## Projeto

DataBoard Reports

## Repositório local sugerido

spreadsheet-dashboard-platform

## Descrição geral

O DataBoard Reports será uma plataforma web desenvolvida em Python com Flask para permitir que empresas façam upload de planilhas CSV ou Excel, visualizem dashboards automáticos, gerem gráficos interativos e exportem relatórios em PDF.

O projeto está sendo construído em entregas pequenas e sequenciais, com foco em portfólio profissional para GitHub e divulgação no LinkedIn.

## Stack principal planejada

- Python
- Flask
- Pandas
- Plotly
- SQLite
- SQLAlchemy
- ReportLab
- HTML/CSS
- Bootstrap
- Docker
- Pytest
- Git/GitHub

## Entrega atual

Conversa 1 — Base inicial Flask

## Objetivo da entrega atual

Criar a fundação inicial do projeto Flask, mantendo o escopo pequeno, limpo e profissional.

## O que foi implementado nesta entrega

- Estrutura inicial de pastas.
- Application factory do Flask.
- Página inicial.
- Template base.
- CSS inicial.
- Arquivo de configuração centralizado.
- Arquivo requirements.txt.
- Arquivo .gitignore.
- Arquivo .env.example.
- Dockerfile inicial.
- docker-compose.yml inicial.
- README.md inicial.
- Arquivos placeholder para futuras camadas de serviço.
- Testes mínimos de importação para os módulos de serviço.
- Pastas uploads, reports e sample_data versionadas com .gitkeep.

## Funcionalidades ainda não implementadas

- Upload de arquivos.
- Leitura de CSV.
- Leitura de Excel.
- Validação de planilhas.
- Banco de dados.
- Modelos SQLAlchemy.
- Gráficos com Plotly.
- Dashboard dinâmico.
- Histórico de arquivos processados.
- Exportação de relatórios em PDF.
- Autenticação.
- Deploy em nuvem.
- Pipeline CI/CD.

## Arquitetura atual

A aplicação usa o padrão application factory do Flask.

Arquivo principal:

- run.py

Pacote principal:

- app/

Arquivos centrais:

- app/__init__.py
- app/config.py
- app/routes.py
- app/models.py

Templates:

- app/templates/base.html
- app/templates/index.html
- app/templates/upload.html
- app/templates/dashboard.html
- app/templates/history.html

Arquivos estáticos:

- app/static/css/style.css

Camada de serviços preparada:

- app/services/data_loader.py
- app/services/analyzer.py
- app/services/charts.py
- app/services/reports.py

Pastas preparadas para arquivos futuros:

- app/uploads/
- app/reports/
- sample_data/

## Rotas existentes

### GET /

Renderiza a página inicial da aplicação.

Função responsável:

- index()

Arquivo:

- app/routes.py

## Decisões técnicas tomadas

- O projeto usará Flask com application factory para facilitar testes, organização e evolução.
- A configuração foi centralizada em app/config.py.
- As funcionalidades futuras foram separadas em uma camada de services.
- Uploads e relatórios gerados terão pastas próprias.
- Banco de dados ainda não foi implementado para manter a primeira entrega simples.
- Os templates de upload, dashboard e histórico foram criados apenas como placeholders.
- O menu exibe funcionalidades futuras como itens desabilitados.
- Bootstrap foi usado via CDN para acelerar a criação visual inicial.
- CSS customizado foi criado em app/static/css/style.css.
- Dockerfile e docker-compose.yml foram adicionados de forma inicial, sem configurações avançadas.
- Testes iniciais validam apenas a existência/importação de módulos planejados.

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

```bash
pytest
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
│   ├── test_data_loader.py
│   └── test_analyzer.py
│
├── sample_data/
│   └── .gitkeep
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── PROJECT_STATE.md
└── run.py
```

## Próxima entrega sugerida

Conversa 2 — Upload de arquivos CSV e Excel

## Objetivo sugerido para a próxima conversa

Implementar a tela de upload de planilhas, ainda de forma simples e controlada.

## Escopo sugerido para a próxima entrega

- Criar rota GET /upload.
- Criar rota POST /upload.
- Ativar o link Upload no menu.
- Criar formulário HTML para envio de arquivo.
- Validar extensões permitidas: .csv, .xlsx e .xls.
- Salvar arquivos enviados em app/uploads.
- Exibir mensagens de sucesso e erro.
- Não processar os dados ainda.
- Não criar dashboard ainda.
- Não criar banco de dados ainda.
- Adicionar testes básicos para validação de extensão.
- Atualizar README.md.
- Atualizar PROJECT_STATE.md.

## Prompt recomendado para iniciar a próxima conversa

Vamos iniciar a Conversa 2 do projeto DataBoard Reports.

Use como base o PROJECT_STATE.md da conversa anterior.

Agora quero implementar apenas a funcionalidade inicial de upload de arquivos CSV e Excel.

Regras:
- Não implemente dashboard ainda.
- Não implemente banco de dados ainda.
- Não implemente gráficos ainda.
- Não implemente relatório PDF ainda.
- Mantenha a entrega pequena e profissional.
- Crie rota GET /upload.
- Crie rota POST /upload.
- Ative o link Upload no menu.
- Crie formulário HTML para upload.
- Valide extensões permitidas: .csv, .xlsx e .xls.
- Salve arquivos em app/uploads.
- Mostre mensagens de sucesso e erro usando flash messages do Flask.
- Crie testes básicos para validação de extensão.
- Atualize o README.md.
- Atualize o PROJECT_STATE.md ao final.

Entregue os arquivos completos e explique onde cada um deve ficar.