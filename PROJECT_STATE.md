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
* Kaleido
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

Conversa 17 — Persistência dos relatórios gerados

### Objetivo da entrega atual

Criar uma camada de persistência para registrar cada relatório PDF gerado, relacionando o relatório ao upload que lhe deu origem.

A entrega transforma os arquivos PDF em entidades persistentes do sistema, permitindo consultar os relatórios já gerados, exibi-los na página de detalhes do upload e realizar novamente o download sem precisar recriar o documento.

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

### Conversa 13 — Inclusão da análise automática no relatório PDF

* Serviço `app/services/reports.py` atualizado para receber o resultado da análise automática.
* Função `generate_upload_report()` atualizada para receber:
  * registro do upload;
  * resultado da análise;
  * pasta de relatórios.
* Resultado de `analyze_dataframe()` integrado à geração do PDF.
* Função auxiliar criada para converter diferentes formatos de resultado de análise em dicionário.
* Função auxiliar `_build_analysis_summary()` criada.
* Resumo estruturado da análise automática implementado.
* PDF atualizado para exibir:
  * quantidade de colunas numéricas;
  * quantidade de colunas categóricas/texto;
  * quantidade total de valores ausentes;
  * nomes das colunas numéricas;
  * nomes das colunas categóricas/texto.
* Seção “Valores ausentes por coluna” adicionada ao relatório.
* Quantidade de valores ausentes por coluna adicionada.
* Percentual de valores ausentes por coluna adicionado.
* Mensagem específica criada para planilhas sem valores ausentes.
* Tratamento de listas vazias de colunas implementado.
* Quebra automática de listas longas de colunas mantida no PDF.
* Caracteres especiais nos nomes das colunas tratados com escape.
* Data de geração passou a ser calculada uma única vez para uso no nome e no conteúdo do relatório.
* Função reutilizável `get_existing_upload_file_path()` criada em `app/routes.py`.
* Validação do caminho físico padronizada com `Path.is_file()`.
* Dependência direta de `os.path.exists()` removida das rotas.
* Rota de reprocessamento atualizada para usar a validação compartilhada de arquivo físico.
* Rota GET `/history/<int:record_id>/report` atualizada.
* Arquivo original passou a ser recarregado antes da geração do relatório.
* Serviço `load_spreadsheet()` passou a ser reutilizado pela rota do relatório.
* Serviço `analyze_dataframe()` passou a ser reutilizado pela rota do relatório.
* Geração do PDF bloqueada quando o arquivo físico não existe.
* Redirecionamento para a página de detalhes implementado quando o arquivo não é encontrado.
* Mensagem amigável exibida quando o arquivo original não está disponível.
* Tratamento para tipo de arquivo salvo não suportado implementado.
* Testes de relatório atualizados para a nova assinatura de `generate_upload_report()`.
* DataFrames reais passaram a ser usados nos testes do relatório.
* Teste do resumo de colunas numéricas e categóricas criado.
* Teste do cálculo de valores ausentes criado.
* Teste para análise sem valores ausentes criado.
* Teste da rota de download atualizado para criar um arquivo CSV físico temporário.
* Teste para geração de relatório com arquivo físico inexistente criado.
* Teste confirmou que nenhum PDF é criado quando o arquivo original não existe.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `48 passed`.

### Conversa 14 — Inclusão das estatísticas numéricas no relatório PDF

* Serviço `app/services/reports.py` atualizado.
* Relatório PDF evoluído para apresentar estatísticas das colunas numéricas.
* Campo `numeric_statistics` de `DataAnalysisResult` reutilizado diretamente.
* Nenhum cálculo estatístico duplicado foi implementado no serviço de relatórios.
* Função `_build_numeric_statistics()` criada.
* Estatísticas numéricas organizadas para apresentação no PDF.
* Função `_format_number()` criada.
* Formatação numérica padronizada implementada.
* Valores inteiros passaram a ser exibidos sem casas decimais desnecessárias.
* Separador de milhar no padrão brasileiro implementado.
* Separador decimal com vírgula implementado.
* Valores decimais passaram a ser exibidos com duas casas.
* Valores estatísticos `None` passaram a ser exibidos como `Não disponível`.
* Nova seção “Estatísticas das colunas numéricas” adicionada ao relatório PDF.
* Tabela de estatísticas criada com as colunas:
  * coluna;
  * média;
  * mediana;
  * mínimo;
  * máximo.
* Tratamento para planilhas sem colunas numéricas implementado.
* Mensagem específica adicionada quando nenhuma coluna numérica é identificada.
* Função reutilizável `_apply_data_table_style()` criada.
* Estilo das tabelas de dados centralizado.
* Tabela de valores ausentes passou a reutilizar o estilo compartilhado.
* Testes de formatação numérica criados.
* Teste para números inteiros criado.
* Teste para números decimais criado.
* Teste para valor `None` criado.
* Teste da preparação das estatísticas numéricas criado.
* Teste para planilha sem colunas numéricas criado.
* Teste de geração de PDF sem colunas numéricas criado.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `54 passed`.

### Conversa 15 — Inserção de gráficos no relatório PDF

* Dependência `Kaleido` adicionada ao projeto.
* Restrição de versão do Plotly atualizada.
* Plotly atualizado para versão compatível com Kaleido.
* Ambiente validado com:
  * Plotly `6.9.0`;
  * Kaleido instalado com sucesso.
* Serviço `app/services/charts.py` refatorado.
* Responsabilidades do serviço de gráficos atualizadas.
* Lógica de construção dos gráficos separada da lógica de saída.
* Função `_build_categorical_bar_figure()` criada.
* Função `_build_numeric_histogram_figure()` criada.
* A mesma figura Plotly passou a ser reutilizada para:
  * HTML interativo no dashboard;
  * imagem PNG no relatório PDF.
* Classe `StaticChartResult` criada.
* `StaticChartResult` passou a armazenar:
  * título;
  * tipo do gráfico;
  * nome da coluna;
  * imagem em bytes.
* Função `_to_plotly_image_bytes()` criada.
* Exportação de figuras Plotly para PNG em memória implementada.
* Nenhum arquivo PNG temporário passou a ser necessário.
* Layout dos gráficos separado por contexto.
* Função `_apply_dark_layout()` mantida para o dashboard.
* Função `_apply_report_layout()` criada para o relatório PDF.
* Gráficos do dashboard mantidos com visual dark.
* Gráficos do PDF passaram a utilizar fundo claro e maior legibilidade para impressão.
* Função `generate_categorical_bar_chart_image()` criada.
* Função `generate_numeric_histogram_image()` criada.
* Função `generate_automatic_chart_images()` criada.
* Gráfico de barras categórico passou a poder ser exportado como PNG.
* Histograma numérico passou a poder ser exportado como PNG.
* Serviço `app/services/reports.py` atualizado.
* Suporte a `chart_results` adicionado à função `generate_upload_report()`.
* Argumento `chart_results` mantido como opcional para preservar compatibilidade.
* Importação de `BytesIO` adicionada.
* Integração com `reportlab.platypus.Image` implementada.
* Função `_build_chart_elements()` criada.
* Imagens PNG passaram a ser inseridas diretamente no PDF a partir da memória.
* Componente `KeepTogether` utilizado para manter título e gráfico juntos quando possível.
* Nova seção “Visualizações gráficas” adicionada ao relatório PDF.
* Relatório passou a exibir:
  * gráfico de barras para a primeira coluna categórica compatível;
  * histograma para a primeira coluna numérica compatível.
* Mensagem específica criada para planilhas sem gráficos compatíveis.
* Rota de geração de relatório atualizada.
* Função `generate_automatic_chart_images()` integrada à rota `/history/<int:record_id>/report`.
* Fluxo completo da geração do relatório passou a ser:
  * carregar arquivo;
  * analisar DataFrame;
  * gerar imagens dos gráficos;
  * gerar PDF;
  * retornar o arquivo para download.
* Testes de gráficos expandidos de 5 para 10.
* Teste de geração de PNG do gráfico categórico criado.
* Teste de geração de PNG do histograma criado.
* Assinatura binária real de arquivos PNG validada.
* Teste de geração automática de múltiplas imagens criado.
* Teste para DataFrame vazio criado.
* Teste de entrada inválida para geração estática criado.
* Testes de relatórios expandidos de 11 para 13.
* Teste de inclusão de um gráfico estático no PDF criado.
* Teste de inclusão de múltiplos gráficos no PDF criado.
* Testes do serviço de relatórios passaram a usar uma pequena imagem PNG válida em memória.
* Testes de Plotly/Kaleido mantidos separados dos testes de ReportLab.
* Fluxo real Plotly → Kaleido → PNG validado.
* Fluxo PNG → ReportLab → PDF validado.
* Fluxo completo CSV → Pandas → Plotly → Kaleido → PNG → ReportLab → PDF validado pela suíte integrada.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `61 passed`.

### Conversa 16 — Inserção da prévia dos dados no relatório PDF

* Serviço `app/services/reports.py` atualizado.
* Suporte a DataFrame adicionado à função `generate_upload_report()`.
* Novo argumento opcional `dataframe` adicionado ao serviço de relatórios.
* DataFrame já carregado pela rota passou a ser reutilizado na geração do PDF.
* Nenhuma nova leitura do arquivo foi necessária para gerar a prévia.
* Dependência do Pandas adicionada ao serviço de relatórios.
* Configurações de limite da prévia criadas:
  * máximo de 5 linhas;
  * máximo de 6 colunas;
  * máximo de 40 caracteres por célula.
* Função `_format_preview_value()` criada.
* Valores ausentes passaram a ser exibidos como `-`.
* Valores normais passaram a ser convertidos para texto.
* Textos longos passaram a ser truncados com reticências.
* Função `_build_dataframe_preview()` criada.
* Limitação de linhas da prévia implementada.
* Limitação de colunas da prévia implementada.
* Quantidade total de linhas registrada na estrutura da prévia.
* Quantidade total de colunas registrada na estrutura da prévia.
* Quantidade de linhas exibidas registrada.
* Quantidade de colunas exibidas registrada.
* Quantidade de linhas omitidas calculada.
* Quantidade de colunas omitidas calculada.
* Validação de entrada implementada para garantir uso de `pandas.DataFrame`.
* Validação de limites negativos implementada.
* Nova seção “Prévia dos dados” adicionada ao relatório PDF.
* Tabela de prévia criada com cabeçalho e células formatadas.
* Largura das colunas calculada dinamicamente.
* Cabeçalho da tabela repetido automaticamente em caso de quebra de página.
* Nota informativa adicionada com a quantidade de linhas e colunas exibidas.
* Mensagem adicionada quando a prévia é limitada para preservar a legibilidade.
* Tratamento implementado para ausência de DataFrame.
* Tratamento implementado para planilha sem colunas.
* Tratamento implementado para planilha sem linhas.
* Rota de geração do relatório atualizada.
* DataFrame passou a ser enviado diretamente para `generate_upload_report()`.
* Testes de relatórios expandidos de 13 para 19.
* Teste de tratamento de valores ausentes criado.
* Teste de formatação de valores regulares criado.
* Teste de truncamento de texto longo criado.
* Teste de limite de linhas e colunas criado.
* Teste de contabilização de dados omitidos criado.
* Teste de formatação de valores ausentes na prévia criado.
* Teste de rejeição de entrada inválida criado.
* Teste de geração real do PDF com prévia criado.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `67 passed`.

### Conversa 17 — Persistência dos relatórios gerados

* Modelo `ReportRecord` criado.
* Tabela `report_records` criada.
* Relacionamento entre `UploadRecord` e `ReportRecord` implementado.
* Um upload passou a poder possuir vários relatórios.
* Cada relatório passou a manter referência ao upload que lhe deu origem.
* Campo `upload_id` criado como chave estrangeira para `upload_records.id`.
* Campo `file_name` criado para armazenar o nome do arquivo PDF.
* Campo `file_path` criado para armazenar o caminho físico do relatório.
* Campo `created_at` criado para registrar a data e hora de geração.
* Índice adicionado ao campo `upload_id`.
* Relacionamento `UploadRecord.reports` criado.
* Relacionamento `ReportRecord.upload` criado.
* Configuração `cascade="all, delete-orphan"` adicionada ao relacionamento.
* Serviço `app/services/report_history.py` criado.
* Função `create_report_record()` criada.
* Persistência de relatórios com commit e rollback implementada.
* Função `list_report_records_by_upload()` criada.
* Relatórios passaram a ser listados do mais recente para o mais antigo.
* Função `get_report_record()` criada.
* Rota de geração de relatório atualizada.
* Registro no banco passou a ocorrer somente após a geração bem-sucedida do PDF.
* Nome e caminho físico do PDF gerado passaram a ser persistidos.
* Página de detalhes do upload atualizada.
* Relatórios relacionados ao upload passaram a ser enviados ao template.
* Nova seção “Relatórios PDF” adicionada à página de detalhes.
* Nome, ID e data de geração dos relatórios passaram a ser exibidos.
* Estado vazio criado para uploads que ainda não possuem relatórios.
* Link “Baixar PDF” adicionado para cada relatório persistido.
* Rota GET `/reports/<int:report_id>/download` criada.
* Download de relatórios existentes implementado.
* Tratamento 404 criado para relatório inexistente.
* Validação da existência física do PDF implementada.
* Mensagem amigável adicionada quando o arquivo físico do relatório não existe mais.
* Redirecionamento para a página de detalhes do upload implementado quando o PDF não é encontrado.
* Pasta temporária de relatórios adicionada à configuração dos testes.
* Testes deixaram de gerar PDFs dentro da pasta real da aplicação.
* Arquivo `tests/test_report_history.py` criado.
* Teste de persistência de relatório criado.
* Teste do relacionamento entre upload e relatório criado.
* Teste da listagem de relatórios por upload criado.
* Teste da busca individual de relatório criado.
* Teste de integração entre geração física e persistência criado.
* Teste de exibição dos relatórios na página de detalhes criado.
* Teste do estado vazio de relatórios criado.
* Teste de download de relatório existente criado.
* Teste de erro 404 para relatório inexistente criado.
* Teste para arquivo físico de relatório inexistente criado.
* Correção de recuo realizada na seção “Prévia dos dados” do relatório PDF.
* A prévia do PDF passou a ser inserida corretamente mesmo quando a planilha não possui colunas numéricas.
* Todos os testes anteriores permaneceram funcionando.
* O comando `python -m pytest` retornou `76 passed`.


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
│   ├── test_reports.py
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
```
## Arquivos modificados na Conversa 13

```text
app/services/reports.py
app/routes.py
tests/test_reports.py
tests/test_history.py
PROJECT_STATE.md
```
## Arquivos modificados na Conversa 14

```text
app/services/reports.py
tests/test_reports.py
PROJECT_STATE.md
```

## Arquivos modificados na Conversa 15
```text
requirements.txt
app/services/charts.py
app/services/reports.py
app/routes.py
tests/test_charts.py
tests/test_reports.py
PROJECT_STATE.md
```
## Arquivos modificados na Conversa 16

```text
app/services/reports.py
app/routes.py
tests/test_reports.py
PROJECT_STATE.md
```
## Arquivos modificados na Conversa 17

```text
app/models.py
app/routes.py
app/services/reports.py
app/services/report_history.py
app/templates/upload_detail.html
conftest.py
tests/test_history.py
tests/test_report_history.py
PROJECT_STATE.md
```


```markdown
## Resultado atual dos testes

Comando executado:

```bash
python -m pytest
```

Resultado validado na Conversa 17:

```text
76 passed in 23.28s
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
* validar o comportamento com 67 testes automatizados.
* gerar um relatório PDF básico a partir de um upload registrado;
* salvar relatórios gerados na pasta `app/reports/`;
* baixar o relatório PDF pelo navegador;
* gerar nomes seguros e únicos para os relatórios;
* exibir no PDF os principais metadados do upload;
* formatar datas e horários no relatório;
* quebrar nomes longos de arquivos em múltiplas linhas;
* receber erro 404 ao solicitar relatório de upload inexistente;
* acessar a geração de PDF pela página de detalhes do upload;
* recarregar o arquivo original antes de gerar o relatório PDF;
* validar a existência física do arquivo antes da geração do PDF;
* reutilizar o serviço de carregamento de planilhas na geração do relatório;
* reutilizar o serviço de análise automática na geração do relatório;
* exibir no PDF a quantidade de colunas numéricas;
* exibir no PDF a quantidade de colunas categóricas/texto;
* exibir no PDF os nomes das colunas numéricas;
* exibir no PDF os nomes das colunas categóricas/texto;
* exibir no PDF a quantidade total de valores ausentes;
* exibir no PDF os valores ausentes por coluna;
* exibir no PDF o percentual de valores ausentes por coluna;
* exibir mensagem no PDF quando não houver valores ausentes;
* impedir a geração do relatório quando o arquivo original não existir;
* redirecionar o usuário para os detalhes do upload quando o arquivo original não for encontrado;
* manter a geração de PDF protegida contra registros inexistentes com resposta 404.
* reutilizar as estatísticas numéricas calculadas pelo serviço `analyzer.py`;
* exibir no PDF a média das colunas numéricas;
* exibir no PDF a mediana das colunas numéricas;
* exibir no PDF o valor mínimo das colunas numéricas;
* exibir no PDF o valor máximo das colunas numéricas;
* formatar números inteiros sem casas decimais desnecessárias;
* formatar números decimais com duas casas;
* utilizar separadores numéricos no padrão brasileiro;
* tratar estatísticas indisponíveis;
* gerar normalmente o relatório quando a planilha não possui colunas numéricas;
* gerar versões estáticas dos gráficos Plotly;
* exportar gráficos Plotly para imagens PNG com Kaleido;
* manter as imagens dos gráficos em memória;
* gerar gráfico de barras estático para a primeira coluna categórica compatível;
* gerar histograma estático para a primeira coluna numérica compatível;
* reutilizar a mesma lógica de construção de gráficos no dashboard e no PDF;
* manter o dashboard com gráficos interativos;
* inserir gráficos estáticos no relatório PDF;
* exibir uma seção de visualizações gráficas no relatório;
* gerar normalmente o PDF quando não existem gráficos compatíveis;
* executar o fluxo completo de geração de relatório com análise, estatísticas e gráficos.
* reutilizar o DataFrame já carregado para gerar a prévia do relatório;
* inserir uma prévia dos dados no PDF;
* limitar a prévia a 5 linhas;
* limitar a prévia a 6 colunas;
* truncar textos longos nas células;
* exibir valores ausentes como `-`;
* informar quantas linhas e colunas estão sendo exibidas;
* informar quando a prévia foi limitada;
* gerar normalmente o relatório quando a planilha não possui linhas ou colunas disponíveis para prévia.
* registrar cada relatório PDF gerado no banco SQLite;
* relacionar cada relatório ao upload que lhe deu origem;
* armazenar o nome do arquivo PDF;
* armazenar o caminho físico do relatório;
* armazenar a data e hora de geração do relatório;
* consultar os relatórios relacionados a um upload;
* listar os relatórios do mais recente para o mais antigo;
* exibir os relatórios na página de detalhes do upload;
* exibir um estado vazio quando nenhum relatório foi gerado;
* baixar novamente um relatório já existente;
* impedir o download de registros de relatório inexistentes;
* informar quando o registro existe, mas o arquivo físico do PDF não está mais disponível;
* manter a geração física do PDF separada da persistência dos relatórios;
* validar o comportamento da aplicação com 76 testes automatizados.

---

## O que ainda não foi implementado

* Persistência da análise automática completa.
* Persistência dos gráficos gerados.
* Persistência da prévia da planilha.
* Página geral de histórico de relatórios.
* Exclusão de relatórios.
* Exclusão de registros de upload.
* Autenticação.
* Deploy.
* Pipeline CI/CD.
* Filtros avançados.
* Dashboards customizáveis.
* Upload múltiplo.
* Edição de registros de histórico.
* Migrações profissionais de banco com Flask-Migrate.
* Permissões por usuário.


---

## Próxima entrega sugerida

Conversa 18 — Histórico geral de relatórios gerados

## Objetivo provável da Conversa 18

Criar uma página central para consultar todos os relatórios PDF gerados pela aplicação, independentemente do upload de origem.

Essa entrega permitirá visualizar os documentos gerados em um histórico próprio, identificar o arquivo de origem e acessar novamente cada relatório.

## Escopo recomendado para a Conversa 18

* Criar função para listar todos os relatórios persistidos.
* Carregar o upload relacionado junto com cada relatório.
* Criar rota GET `/reports`.
* Criar template `reports_history.html`.
* Adicionar o item “Relatórios” ao menu principal.
* Exibir:

  * ID do relatório;
  * nome do PDF;
  * upload de origem;
  * data e hora de geração;
  * link para os detalhes do upload;
  * link para download do PDF.
* Criar estado vazio para ausência de relatórios.
* Criar testes do serviço de listagem.
* Criar testes da página geral de relatórios.
* Criar testes dos links de navegação e download.
* Manter a ordenação do mais recente para o mais antigo.

## Manter fora do escopo da Conversa 18

* Exclusão de relatórios.
* Regeneração automática de relatórios.
* Versionamento de relatórios.
* Filtros avançados.
* Autenticação.
* Permissões por usuário.
* Deploy.


---
## Observação de continuidade

A Conversa 17 concluiu a persistência dos relatórios PDF gerados.

O projeto agora possui um fluxo funcional para:

1. receber uma planilha;
2. validar sua extensão;
3. salvar o arquivo no servidor;
4. carregar os dados com Pandas;
5. extrair metadados;
6. analisar automaticamente a estrutura dos dados;
7. identificar colunas numéricas e categóricas;
8. calcular valores ausentes;
9. calcular estatísticas numéricas;
10. gerar gráficos interativos com Plotly;
11. exibir os gráficos no dashboard;
12. registrar o upload no banco SQLite;
13. salvar o caminho físico do arquivo;
14. listar uploads anteriores;
15. abrir os detalhes de cada upload;
16. reprocessar uploads antigos;
17. recriar o dashboard a partir de arquivos salvos;
18. gerar e baixar relatórios PDF;
19. incluir no PDF os metadados do upload;
20. incluir no PDF o resumo da análise automática;
21. apresentar valores ausentes e percentuais por coluna;
22. apresentar estatísticas das colunas numéricas;
23. gerar versões estáticas dos gráficos com Plotly e Kaleido;
24. inserir gráficos estáticos no PDF;
25. inserir uma prévia limitada dos dados da planilha;
26. tratar valores ausentes e textos longos na prévia;
27. informar os limites aplicados à prévia;
28. impedir a geração do relatório quando o arquivo original não existe;
29. registrar no banco cada relatório gerado;
30. relacionar relatórios aos respectivos uploads;
31. listar os relatórios na página de detalhes do upload;
32. baixar novamente relatórios já existentes;
33. tratar registros e arquivos físicos de relatórios inexistentes;
34. validar o comportamento com 76 testes automatizados.

A partir da Conversa 18, o projeto deverá evoluir para uma página geral de histórico de relatórios gerados.
