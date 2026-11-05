import getpass
import sqlite3
from contextlib import closing
from pathlib import Path
 
from seguranca import gerar_hash_senha
 
DB_PATH = Path(__file__).with_name("gestao_produtos.db")
 
 
def main():
    login = input("Novo usuário: ").strip()
    senha = getpass.getpass("Senha (mínimo 8 caracteres): ")
    confirmacao = getpass.getpass("Repita a senha: ")
 
    if not login:
        raise SystemExit("O nome de usuário não pode ficar vazio.")
    if len(senha) < 8:
        raise SystemExit("A senha deve ter pelo menos 8 caracteres.")
    if senha != confirmacao:
        raise SystemExit("As senhas não conferem.")
 
    senha_hash, salt = gerar_hash_senha(senha)
 
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:  # commit automático; rollback em caso de erro
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Usuario (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL,
                    salt TEXT NOT NULL
                );
            """)
            try:
                conn.execute(
                    "INSERT INTO Usuario (login, senha_hash, salt) VALUES (?, ?, ?);",
                    (login, senha_hash, salt),
                )
            except sqlite3.IntegrityError:
                raise SystemExit(f"O usuário '{login}' já existe.")
 
    print(f"Usuário '{login}' criado com sucesso.")
 
 
if __name__ == "__main__":
    main()