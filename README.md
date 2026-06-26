# DataBoard Reports

Plataforma web para upload de planilhas CSV ou Excel, geração automática de dashboards interativos e exportação de relatórios em PDF.

## Objetivo

O objetivo do DataBoard Reports é demonstrar, em um projeto profissional de portfólio, a construção de uma aplicação web com Python, Flask, Pandas, Plotly, SQLite, SQLAlchemy, ReportLab, Docker e boas práticas de engenharia de software.

Nesta primeira entrega, o projeto contém apenas a base inicial da aplicação Flask.

## Stack planejada

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

## Funcionalidades planejadas

- Upload de arquivos CSV e Excel.
- Leitura de planilhas com Pandas.
- Análise automática de dados.
- Geração de dashboards interativos com Plotly.
- Histórico de arquivos processados.
- Exportação de relatórios em PDF.
- Execução com Docker.
- Testes automatizados.

## Funcionalidades disponíveis nesta entrega

- Estrutura inicial do projeto.
- Aplicação Flask com application factory.
- Página inicial.
- Template base.
- CSS inicial.
- Arquivo de configuração.
- Requirements.
- Dockerfile inicial.
- docker-compose inicial.
- Testes mínimos de importação.

## Como rodar localmente

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd spreadsheet-dashboard-platform
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual:

No Windows:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

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

Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Como rodar com Docker

Construa e execute o container:

```bash
docker compose up --build
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Como rodar os testes

```bash
pytest
```

## Status do projeto

Entrega atual: base inicial Flask.

Próxima entrega sugerida: implementação da tela de upload e validação inicial de arquivos CSV/Excel.