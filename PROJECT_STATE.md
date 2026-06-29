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

## Entrega atual

Conversa 3 — Leitura inicial de arquivos com Pandas

## Objetivo da entrega atual

Implementar a leitura inicial de arquivos CSV e Excel usando Pandas, criando uma camada de serviço simples e testável para carregar planilhas e retornar metadados básicos.

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

## Arquivos modificados na Conversa 3

* app/services/data_loader.py
* tests/test_data_loader.py
* README.md
* PROJECT_STATE.md
* requirements.txt

## Comando para executar a aplicação

```bash
python run.py
```

## Comando para executar os testes

```bash
python -m pytest
```

## Resultado esperado dos testes

Todos os testes devem passar.

## O que ainda não foi implementado

* Dashboard.
* Gráficos interativos.
* Integração da leitura da planilha com a interface web.
* Exibição da prévia dos dados no navegador.
* Banco de dados.
* SQLAlchemy.
* Histórico de uploads.
* Geração de PDF.
* Autenticação.
* Deploy.
* Pipeline CI/CD.

## Próxima entrega sugerida

Conversa 4 — Exibir uma prévia dos dados carregados na interface web.

## Objetivo provável da Conversa 4

Integrar a camada de leitura criada na Conversa 3 com o fluxo de upload criado na Conversa 2, permitindo que, após o envio de um arquivo válido, o sistema exiba uma página simples com os metadados e uma prévia dos dados carregados.

## Escopo recomendado para a Conversa 4

* Atualizar a rota POST /upload para carregar a planilha após salvar o arquivo.
* Usar load_spreadsheet_metadata para extrair os metadados.
* Criar ou atualizar dashboard.html apenas como tela de prévia simples.
* Exibir:

  * nome do arquivo;
  * quantidade de linhas;
  * quantidade de colunas;
  * nomes das colunas;
  * primeiras linhas.
* Manter o escopo limitado à prévia dos dados.
* Não implementar gráficos ainda.
* Não implementar Plotly ainda.
* Não implementar banco de dados ainda.
* Não implementar histórico ainda.
* Não implementar PDF ainda.
* Criar testes para o fluxo básico de upload com leitura de metadados.
