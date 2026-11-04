import sqlite3
from contextlib import closing
from pathlib import Path
 
DB_PATH = Path(__file__).resolve().parent / "gestao_produtos.db"
 
QUERY_RANKING = """
SELECT
    p.nome AS produto,
    c.nome_categoria AS categoria,
    p.preco AS preco_unitario,
    COALESCE(SUM(v.quantidade), 0) AS total_vendido,
    COALESCE(SUM(v.quantidade * p.preco), 0.0) AS faturamento_total,
    p.estoque AS estoque_restante
FROM Produto p
LEFT JOIN Vendas v ON p.id_produto = v.id_produto
LEFT JOIN Categoria c ON p.id_categoria = c.id_categoria
GROUP BY p.id_produto, p.nome, p.preco, p.estoque, c.nome_categoria
ORDER BY total_vendido DESC;
"""
 
 
def abrir_conexao() -> sqlite3.Connection:
    """Abre o banco com chaves estrangeiras ativas e linhas acessíveis por nome."""
    if not DB_PATH.exists():
        # Sem esta checagem, o SQLite criaria um banco vazio em silêncio
        raise FileNotFoundError(f"Banco de dados não encontrado: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn
 
 
def consultar_ranking() -> list[dict]:
    """Devolve o ranking de vendas como lista de dicionários."""
    with closing(abrir_conexao()) as conn:
        return [dict(linha) for linha in conn.execute(QUERY_RANKING)]