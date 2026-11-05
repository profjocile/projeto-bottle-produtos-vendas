import functools
import os
import secrets
from pathlib import Path

from bottle import (
    TEMPLATE_PATH,
    Bottle,
    redirect,
    request,
    response,
    run,
    static_file,
    template,
)

from dados import buscar_usuario, consultar_ranking
from seguranca import verificar_senha

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH.insert(0, str(BASE_DIR / "views"))
 
# O segredo vem do ambiente. Sem ele, usa-se um valor aleatório temporário,
# e todas as sessões são invalidadas a cada reinício do servidor.
CHAVE_SECRETA = os.environ.get("APP_SECRET") or secrets.token_hex(32)
NOME_COOKIE = "sessao"
 
# A URL carrega apenas um código; a mensagem real fica no servidor
MENSAGENS = {
    "restrito": "Acesso restrito. Faça login para continuar.",
    "invalido": "Usuário ou senha incorretos.",
    "saiu": "Sessão encerrada.",
}
 
app = Bottle()
 
 
def ir_para_login(codigo: str):
    redirect(f"/login?erro={codigo}")
 
 
def requer_autenticacao(funcao_rota):
    """Bloqueia a rota se o cookie de sessão estiver ausente ou adulterado."""
    @functools.wraps(funcao_rota)
    def wrapper(*args, **kwargs):
        usuario = request.get_cookie(NOME_COOKIE, secret=CHAVE_SECRETA)
        if not usuario:
            ir_para_login("restrito")
        return funcao_rota(*args, **kwargs)
    return wrapper
 
 
@app.get("/login")
def exibir_login():
    codigo = request.query.get("erro", "")
    return template("login", mensagem=MENSAGENS.get(codigo, ""))
 
 
@app.post("/login")
def processar_login():
    login = (request.forms.getunicode("usuario") or "").strip()
    senha = request.forms.getunicode("senha") or ""  # senha nunca recebe strip()
 
    registro = buscar_usuario(login)
    if registro and verificar_senha(senha, registro["senha_hash"], registro["salt"]):
        response.set_cookie(
            NOME_COOKIE,
            registro["login"],
            secret=CHAVE_SECRETA,
            httponly=True,    # JavaScript não consegue ler o cookie
            samesite="Lax",   # reduz o envio do cookie em requisições de outros sites
            max_age=3600,     # sessão de 1 hora
            path="/",
            # secure=True,    # ative quando o site usar HTTPS
        )
        redirect("/relatorio/ranking")
 
    ir_para_login("invalido")
 
 
@app.get("/logout")
def logout():
    response.delete_cookie(NOME_COOKIE, path="/")
    ir_para_login("saiu")
 
 
@app.get("/relatorio/ranking")
@requer_autenticacao
def pagina_ranking():
    usuario = request.get_cookie(NOME_COOKIE, secret=CHAVE_SECRETA)
    return template("ranking", linhas=consultar_ranking(), usuario=usuario)
 
 
@app.get("/api/ranking-vendas")
def api_ranking_vendas():
    return {"status": "sucesso", "dados": consultar_ranking()}
 
 
@app.get("/static/<caminho:path>")
def arquivos_estaticos(caminho):
    return static_file(caminho, root=str(BASE_DIR / "static"))
 
 
if __name__ == "__main__":
    if "APP_SECRET" not in os.environ:
        print("Aviso: APP_SECRET não definido. Usando segredo temporário.")
    print("Servidor rodando em http://localhost:8080")
    run(app, host="localhost", port=8080, debug=True, reloader=True)