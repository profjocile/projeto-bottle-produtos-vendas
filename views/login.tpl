<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <style>
    body { font-family: Arial, sans-serif; display: flex; justify-content: center;
           align-items: center; height: 100vh; margin: 0; background: #f8f9fa; }
    .card { background: white; padding: 30px; border-radius: 8px; width: 300px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    label { display: block; margin-top: 10px; }
    input { width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; }
    input[type="submit"] { margin-top: 18px; background: #0d6efd; color: white;
                           border: none; font-weight: bold; cursor: pointer; }
    .erro { color: #dc3545; font-size: 0.9em; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Acesso restrito</h2>
    % if mensagem:
    <p class="erro">{{ mensagem }}</p>
    % end
    <form action="/login" method="post">
      <label for="usuario">Usuário</label>
      <input id="usuario" type="text" name="usuario" required autocomplete="username">
 
      <label for="senha">Senha</label>
      <input id="senha" type="password" name="senha" required autocomplete="current-password">
 
      <input type="submit" value="Entrar">
    </form>
  </div>
</body>
</html>