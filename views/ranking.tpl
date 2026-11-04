<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Ranking de vendas</title>
  <style>
    body { font-family: "Segoe UI", Arial, sans-serif; margin: 30px; background: #f8f9fa; }
    h1 { color: #0d6efd; }
    .card-grafico { text-align: center; margin-bottom: 25px; background: white;
                    padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .card-grafico img { max-width: 100%; border-radius: 4px; }
    table { width: 100%; border-collapse: collapse; background: white; }
    th, td { border: 1px solid #dee2e6; padding: 12px; text-align: left; }
    th { background: #0d6efd; color: white; }
    tr:nth-child(even) { background: #f1f3f5; }
  </style>
</head>
<body>
  <h1>Painel e ranking de vendas</h1>
 
  <div class="card-grafico">
    <img src="/static/ranking_vendas.png" alt="Gráfico de barras com a quantidade vendida por produto">
  </div>
 
  <h2>Desempenho por produto</h2>
  <table>
    <tr>
      <th>Produto</th>
      <th>Categoria</th>
      <th>Qtd. vendida</th>
      <th>Faturamento</th>
      <th>Estoque</th>
    </tr>
    % for linha in linhas:
    <tr>
      <td><strong>{{ linha['produto'] }}</strong></td>
      <td>{{ linha['categoria'] }}</td>
      <td>{{ linha['total_vendido'] }} unid.</td>
      <td>R$ {{ "%.2f" % linha['faturamento_total'] }}</td>
      <td>{{ linha['estoque_restante'] }}</td>
    </tr>
    % end
  </table>
</body>
</html>