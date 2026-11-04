from contextlib import closing
from pathlib import Path

from bottle import TEMPLATE_PATH, Bottle, response, run, static_file, template

from dados import abrir_conexao, consultar_ranking

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH.insert(0, str(BASE_DIR / "views"))
 
app = Bottle()
 
 
@app.get("/api/ranking-vendas")
def api_ranking_vendas():
    """Retorna o ranking em JSON. O Bottle converte dicionários em JSON sozinho."""
    return {"status": "sucesso", "dados": consultar_ranking()}
 
 
@app.get("/relatorio/ranking")
def pagina_ranking():
    """Renderiza a página HTML com a tabela e o gráfico."""
    return template("ranking", linhas=consultar_ranking())
 
 
@app.get("/static/<caminho:path>")
def arquivos_estaticos(caminho):
    """Entrega imagens e outros arquivos da pasta static/."""
    return static_file(caminho, root=str(BASE_DIR / "static"))


@app.get("/api/produtos/<id_produto:int>")
def api_produto(id_produto):
    with closing(abrir_conexao()) as conn:
        linha = conn.execute(
            "SELECT id_produto, nome, preco, estoque FROM Produto WHERE id_produto = ?;",
            (id_produto,),
        ).fetchone()
 
    if linha is None:
        response.status = 404
        return {"status": "erro", "mensagem": "Produto não encontrado."}
    return {"status": "sucesso", "dados": dict(linha)}

if __name__ == "__main__":
    print("Servidor rodando em http://localhost:8080")
    run(app, host="localhost", port=8080, debug=True, reloader=True)