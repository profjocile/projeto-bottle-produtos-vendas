# Gestão de Produtos e Vendas — API e relatório web

Projeto desenvolvido como atividade do **Curso de Programador do Senac**. A aplicação utiliza Python e o microframework Bottle para consultar um banco SQLite de produtos e vendas, disponibilizar dados por uma API JSON e apresentar um relatório web com ranking de vendas.

## Objetivos da atividade

- Conectar uma aplicação Python a um banco de dados SQLite.
- Consultar e relacionar dados de produtos, categorias e vendas usando SQL.
- Criar rotas HTTP com Bottle.
- Disponibilizar dados em formato JSON.
- Renderizar uma página HTML com dados do banco e um gráfico.

## Funcionalidades

- **Ranking de vendas:** reúne produtos e categorias, quantidade vendida, faturamento total e estoque restante. Os resultados são ordenados pela quantidade vendida, da maior para a menor.
- **API do ranking:** retorna os dados do ranking em JSON.
- **Consulta de produto:** busca um produto pelo identificador e retorna seus dados em JSON. Quando o produto não existe, a API responde com status HTTP 404.
- **Relatório web:** mostra uma tabela de desempenho por produto e o gráfico disponível em `static/ranking_vendas.png`.

## Tecnologias e estrutura

- **Python** e **Bottle** para a aplicação web e as rotas.
- **SQLite** para armazenamento dos dados.
- **Bottle Templates** para renderização da página HTML.

```text
.
├── app.py                 # Aplicação Bottle e rotas HTTP
├── dados.py               # Conexão SQLite e consulta do ranking
├── gestao_produtos.db     # Banco de dados usado pela aplicação
├── static/
│   └── ranking_vendas.png # Gráfico do relatório
└── views/
    └── ranking.tpl        # Template da página de ranking
```

## Requisitos

- Python 3.9 ou superior.
- A dependência Bottle.

## Como executar

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone https://github.com/profjocile/projeto-bottle-produtos-vendas.git
   cd projeto-bottle-produtos-vendas
   ```

2. (Opcional, recomendado) Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   No Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   No Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Instale o Bottle:

   ```bash
   python -m pip install bottle
   ```

4. Inicie o servidor:

   ```bash
   python app.py
   ```

   Por padrão, a aplicação fica disponível em `http://localhost:8080`. O arquivo `gestao_produtos.db` deve estar na raiz do projeto, junto de `app.py` e `dados.py`.

## Rotas disponíveis

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/ranking-vendas` | Retorna o ranking de vendas em JSON. |
| `GET` | `/api/produtos/{id_produto}` | Retorna os dados do produto com o identificador informado. |
| `GET` | `/relatorio/ranking` | Exibe o relatório HTML com tabela e gráfico. |
| `GET` | `/static/{caminho}` | Disponibiliza arquivos da pasta `static/`. |

Exemplos para testar no navegador, com o servidor em execução:

- Relatório: `http://localhost:8080/relatorio/ranking`
- Ranking em JSON: `http://localhost:8080/api/ranking-vendas`
- Produto de ID 1: `http://localhost:8080/api/produtos/1`

## Como os dados são obtidos

O módulo `dados.py` abre o banco SQLite e executa uma consulta que relaciona as tabelas `Produto`, `Vendas` e `Categoria`. Para produtos sem vendas, a consulta considera os totais como zero. O resultado é convertido em uma lista de dicionários, utilizada tanto pela API quanto pelo template do relatório.

## Observação

Esta aplicação foi preparada para fins didáticos. O servidor é iniciado em modo de depuração (`debug=True`) e escuta apenas em `localhost`; essas configurações são apropriadas para desenvolvimento local, não para publicar a aplicação em produção.
