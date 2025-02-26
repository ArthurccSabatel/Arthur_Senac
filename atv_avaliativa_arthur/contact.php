<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="contact.css">
    <title>contact</title>
    <style>
        body{
            align-items: center;
            display: flex;
            text-align: center;
        }
        table{
            border-collapse: collapse;
            background-color: rgb(198, 179, 142);
            text-align: center;
            border-radius: 5px;
            border-color: black;
            text-align: center;
        }
        .asd{
            color:#333;
        }
        .texto{
            text-align: center;
            font-family: 'Times New Roman', Times, serif;
            font-size: 10px;
        }
    </style>
</head>
    <body>
        <?php

        $conexao = mysqli_connect("localhost", "root","VoucherDev@2024","contato");
        
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {

        if(!$conexao){
            echo "ops!, deu erro".mysqli_connect_error();
        } else {
            echo"";
        }
        
        $nome = isset($_POST['nome']) ? mysqli_real_escape_string($conexao, $_POST['nome']) : '';
        $fone = isset($_POST['fone']) ? mysqli_real_escape_string($conexao, $_POST['fone']) : '';
        $email = isset($_POST['email']) ? mysqli_real_escape_string($conexao, $_POST['email']) : '';
        $comentario = isset($_POST['comentario']) ? mysqli_real_escape_string($conexao, $_POST['comentario']) : '';
        
        $sql = "INSERT INTO info (nome, fone, email, comentario) VALUES ('$nome','$fone', '$email', '$comentario')";
        

        if(mysqli_query($conexao, $sql)){
            echo "<br>";
        } else {
            echo "Erro ao cadastrar informações".mysqli_error($conexao);
        }

        $sql_selecionar = "SELECT * FROM info ORDER BY id DESC LIMIT 1" ;

        $resultado = mysqli_query($conexao, $sql_selecionar);

        if(mysqli_num_rows($resultado) > 0){
        echo"<h2 class='asd'>suas informações:</h2>";

            echo"<table border = '1',border-radius: 10px;>";
            echo"<tr><th>Nome</th><th>fone</th><th>Email</th></tr>";
            while($row = mysqli_fetch_array($resultado)){

                echo "<tr>";
                echo "<td>".htmlspecialchars($row["nome"])."</td>";
                echo "<td>".htmlspecialchars($row["fone"])."</td>";
                echo "<td>".htmlspecialchars($row["email"])."</td>";
                echo "</tr>";

            }
            echo "</table>";
        } else {
            echo "Resultado não encontrado";
        }
        echo"ENTRAREMOS EM CONTATO EM BREVE👍";

        
        mysqli_close($conexao);
        }
        ?>
    </body>
</html>
