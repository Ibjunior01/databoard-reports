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

## Controle das conversas

| Conversa | Entrega                                  | Status    |
| -------- | ---------------------------------------- | --------- |
| 01       | Base inicial Flask                       | Concluída |
| 02       | Upload inicial de arquivos CSV e Excel   | Concluída |
| 03       | Leitura inicial de arquivos com Pandas   | Próxima   |
| 04       | Prévia dos dados carregados na interface | Planejada |
| 05       | Análise automática dos dados             | Planejada |
| 06       | Dashboard inicial                        | Planejada |
| 07       | Gráficos com Plotly                      | Planejada |
| 08       | Histórico de uploads                     | Planejada |
| 09       | Exportação de PDF                        | Planejada |
| 10       | Banco de dados com SQLite/SQLAlchemy     | Planejada |
| 11       | Docker e ajustes finais                  | Planejada |

## O que foi feito na Conversa 1

* Estrutura inicial de pastas criada.
* Aplicação Flask criada com application factory.
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
* O comando `python run.py` funcionou.
* A aplicação abriu corretamente em `http://127.0.0.1:5000`.
* O comando `python -m pytest` retornou testes passando.

## O que foi feito na Conversa 2

* Rota `GET /upload` criada.
* Rota `POST /upload` criada.
* Link Upload ativado no menu do `base.html`.
* Tela profissional de upload criada em `upload.html`.
* Formulário HTML criado com `enctype="multipart/form-data"`.
* Validação de extensões permitidas criada.
* Extensões permitidas nesta etapa:

  * `.csv`
  * `.xlsx`
  * `.xls`
* Arquivos inválidos são recusados antes do salvamento.
* Função `secure_filename` do Werkzeug aplicada ao nome do arquivo.
* Arquivos enviados são salvos em `app/uploads/`.
* Mensagens de sucesso e erro foram implementadas com `flash`.
* CSS da tela de upload foi ajustado para uma identidade visual mais dark/profissional.
* Testes básicos para extensões permitidas foram criados.
* Teste básico para `GET /upload` com status 200 foi criado.
* Teste de upload válido `.csv` criado.
* Teste de bloqueio para arquivo inválido `.pdf` criado.
* O comando `python -m pytest` retornou `13 passed`.
* README.md atualizado.
* PROJECT_STATE.md atualizado.

## Estrutura atual esperada

```txt
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

## Arquivos alterados na Conversa 2

* `app/routes.py`
* `app/templates/base.html`
* `app/templates/upload.html`
* `app/static/css/style.css`
* `tests/test_routes.py`
* `README.md`
* `PROJECT_STATE.md`

## Arquivo criado na Conversa 2

* `tests/test_upload.py`

## Funcionalidade atual

A aplicação permite acessar:

```txt
http://127.0.0.1:5000/upload
```

Na página de upload, o usuário pode enviar arquivos:

* CSV
* Excel `.xlsx`
* Excel `.xls`

Quando o arquivo é válido:

* O nome é tratado com `secure_filename`.
* O arquivo é salvo em `app/uploads/`.
* Uma mensagem de sucesso é exibida.

Quando o arquivo é inválido:

* O arquivo não é salvo.
* Uma mensagem de erro é exibida.

## Testes atuais

O comando:

```bash
python -m pytest
```

retornou:

```txt
13 passed
```

Os testes atuais validam:

* Página inicial respondendo com status 200.
* Página `/upload` respondendo com status 200.
* Extensões permitidas:

  * `.csv`
  * `.xlsx`
  * `.xls`
* Extensões recusadas:

  * `.txt`
  * `.pdf`
  * `.png`
* Arquivo sem extensão recusado.
* Upload válido `.csv` retornando mensagem de sucesso.
* Upload inválido `.pdf` retornando mensagem de erro.
* Testes placeholder das camadas `analyzer` e `data_loader`.

## Importante

Nesta entrega ainda não foi implementado:

* Leitura dos arquivos com Pandas.
* Prévia dos dados na interface.
* Dashboard.
* Gráficos.
* Banco de dados.
* SQLAlchemy.
* Histórico.
* PDF.
* Autenticação.

Esses pontos fazem parte das próximas conversas.

## Como rodar o projeto

Na raiz do projeto:

```bash
python run.py
```

Acessar:

```txt
http://127.0.0.1:5000
```

Página de upload:

```txt
http://127.0.0.1:5000/upload
```

## Como rodar os testes

Na raiz do projeto:

```bash
python -m pytest
```

Resultado esperado:

```txt
13 passed
```

## Commit sugerido para a Conversa 2

```bash
git add .
git commit -m "feat: add spreadsheet upload page"
```

## Próxima conversa

Conversa 3 — Leitura inicial de arquivos com Pandas.

## Objetivo da Conversa 3

Implementar apenas a leitura inicial dos arquivos CSV e Excel enviados ou armazenados em `app/uploads/`.

## Escopo provável da Conversa 3

* Criar ou atualizar funções em `app/services/data_loader.py`.
* Ler arquivos `.csv`, `.xlsx` e `.xls` com Pandas.
* Validar se o arquivo existe antes de tentar ler.
* Validar se a extensão é suportada.
* Retornar informações básicas:

  * quantidade de linhas;
  * quantidade de colunas;
  * nomes das colunas;
  * primeiras linhas.
* Criar testes para leitura de CSV.
* Criar testes para leitura de Excel.
* Criar testes para arquivo inexistente.
* Criar testes para extensão não suportada.
* Atualizar README.md.
* Atualizar PROJECT_STATE.md.

## Regras para a Conversa 3

* Não implementar dashboard ainda.
* Não implementar gráficos ainda.
* Não implementar banco de dados ainda.
* Não implementar SQLAlchemy ainda.
* Não implementar histórico ainda.
* Não implementar PDF ainda.
* Não implementar autenticação ainda.
* Não aumentar o escopo da entrega.
* Manter o código simples, limpo e profissional.

## Próxima entrega após a Conversa 3

Conversa 4 — Exibir uma prévia dos dados carregados na interface web.
