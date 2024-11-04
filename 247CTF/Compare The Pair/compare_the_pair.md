# Compare the Pair

Esse ctf contém uma vulnerabilidade chamada Magic Hash do PHP

## Magic Hash

A vulnerabilidade do Magic Hash consiste em um sistema de comparação de hashes MD5 do PHP:

```php
md5(palavra) == '0e24582370934709437903457...' == 0
```

Uma vez que o hash da palavra é começa com "0e" (0e + numeros) e é seguido de números, o PHP o interpreta como 0x10^(numero), oomo nas notações científicas das calculadoras. 

Ou seja, para qualquer valor de palavra cujo o hash seja "0e + números", o PHP interpretará como valor de hash = 0

Dito isso, sabemo que, a partir do código fonte:

```php
<?php
  require_once('flag.php');
  $password_hash = "0e902564435691274142490923013038";
  $salt = "f789bbc328a3d1a3";
  if(isset($_GET['password']) && md5($salt . $_GET['password']) == $password_hash){
    echo $flag;
  }
  echo highlight_file(__FILE__, true);
?>
```

No CTF o hash começa com 0e e é seguido de números. Agora basta achar uma "password" que, quando somada ao salt, resulte numa string MD5 de "0e + números".

