<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="index.css">
    <title>mercado</title>
    <style>
        body{
            align-items: center;
            display: flex;
        }
        table{
            border-collapse: collapse;
            background-color: azure;
            text-align: center;
            border: 1px solid black;
        }
        .asd{
            color: white;
        }
    </style>
</head>
    <body>
        <?php

        $conexao = mysqli_connect("localhost", "root","VoucherDev@2024","mercado");
        
        // pesquisei como verificar se o formulário foi submetido
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {

        if(!$conexao){
            echo "ops!, deu erro".mysqli_connect_error();
        } else {
            echo"";
        }
        
        // Verificar se os campos POST existem antes de acessá-los e guardando dados do formulário

        $cpf = isset($_POST['cpf']) ? mysqli_real_escape_string($conexao, $_POST['cpf']) : '';
        $cliente = isset($_POST['cliente']) ? mysqli_real_escape_string($conexao, $_POST['cliente']) : '';
        $rg = isset($_POST['rg']) ? mysqli_real_escape_string($conexao, $_POST['rg']) : '';
        $datan = isset($_POST['datan']) ? mysqli_real_escape_string($conexao, $_POST['datan']) : '';
        $ocupacao = isset($_POST['ocupacao']) ? mysqli_real_escape_string($conexao, $_POST['ocupacao']) : '';
        $fone = isset($_POST['fone']) ? mysqli_real_escape_string($conexao, $_POST['fone']) : '';
        $email = isset($_POST['email']) ? mysqli_real_escape_string($conexao, $_POST['email']) : '';
        $cidade = isset($_POST['cidade']) ? mysqli_real_escape_string($conexao, $_POST['cidade']) : '';
        
        $sql = "INSERT INTO cliente (cpf, cliente, rg, datan, ocupacao, fone, email, cidade) VALUES ('$cpf','$cliente','$rg','$datan','$ocupacao','$fone', '$email','$cidade')";
        

        if(mysqli_query($conexao, $sql)){
            echo "<br>CLIENTE cadastrado";
        } else {
            echo "Erro ao cadastrar CLIENTE".mysqli_error($conexao);
        }

        $sql_selecionar = "SELECT * FROM cliente WHERE datan <= 2007-01-01" ;

        $resultado = mysqli_query($conexao, $sql_selecionar);

        if(mysqli_num_rows($resultado) > 0){
        echo"<h2 class='asd'>Clientes Cadastrados:</h2>";

            echo"<table border = '1'>";
            echo"<tr><th>Cliente</th><th>CPF</th><th>RG</th><th>Data</th><th>ocupação</th><th>fone</th><th>Email</th><th>cidade</th></tr>";
            while($row = mysqli_fetch_array($resultado)){

                // htmlspecialchars coverte caractereres especiais
                echo "<tr>";
                echo "<td>".htmlspecialchars($row["cliente"])."</td>";
                echo "<td>".htmlspecialchars($row["cpf"])."</td>";
                echo "<td>".htmlspecialchars($row["rg"])."</td>";
                echo "<td>".htmlspecialchars($row["datan"])."</td>";
                echo "<td>".htmlspecialchars($row["ocupacao"])."</td>";
                echo "<td>".htmlspecialchars($row["fone"])."</td>";
                echo "<td>".htmlspecialchars($row["email"])."</td>";
                echo "<td>".htmlspecialchars($row["cidade"])."</td>";
                echo "</tr>";

            }
            echo "</table>";
        } else {
            echo "Resultado não encontrado";
        }

        
        mysqli_close($conexao);
        }
        ?>
    </body>
</html>
