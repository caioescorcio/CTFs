# Forgotten Pointer File

Nesse CTF, são abordados dois tópicos de vulnerabilidades do PHP:
- Local File Inclusion
- Ponteiros para variáveis locais

# Desafio

Ao iniciar o desafio, nos é mostrado um PHP base com algumas linhas de código:

```php
 <?php
  $fp = fopen("/tmp/flag.txt", "r");
  if($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['include']) && strlen($_GET['include']) <= 10) {
    include($_GET['include']);
  }
  fclose($fp);
  echo highlight_file(__FILE__, true);
?>
```
O raciocínio inical é analisar o que está na lógica do código.

- `$fp = fopen("/tmp/flag.txt", "r");` : é colocada no ponteiro '$fp' o valor da string de flag.txt
- `if($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['include']) && strlen($_GET['include']) <= 10)` : verifica se o método de request para o backend é um GET, se for, espera o argumento da variável "include" e verifica se esse argumento é menor que 10 caracteres.
- `include($_GET['include']);`: se a condição acima for atendida, é incluída no php o arquivo que está no include:

Em relação ao include, caso essa inclusão não esteja devidamente sanitizada, poderá ser feito o acesso a arquivos que antes não eram acessíveis na renderização da página. Vejamos o seguinte exemplo onde o código tenha um "include" sem filtro para o site falso "https://exemplo.com/" :

```php
<?php
if($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['include'])) {
    include($_GET['include']);
  }
?>
```
Nesse caso, como o include pode ser qualquer tipo de string, podemos acessar quaisquer outros tipos de arquivos uma vez que sejam PHP:

`curl -X GET https://exemplo.com/?include=../../pasta/arquivo.php`

Nesse exemplo, adiciona-se a variável `include` à request e colocamos um argumento de um PATH para outro arquivo PHP. Nesse caso, será renderizado o arquivo no diretório `../../pasta/arquivo.php` junto com a página. Para saber mais sobre a vulnerabilidade, acesse o site da [OWASP](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion) sobre isso. 

No exemplo do CTF é difícil acessar um diretório específico, mesmo convertendo-o para PHP devido ao limite de 10 caracteres para a string de include. Não se consegue colocar '/tmp/flag.txt' pois é uma string muito grande.

Assim, vejamos outra vulnerabilidade envolvendo pointeiros no PHP:

Ao colocarmos um valor de alguma variável em um ponteiro PHP, ela fica armazenada na pasta `/proc/NUMERO_DO_PROCESSO_PHP/`, em um servidor linux. Ou seja, em todos os arquivos dentro dessa página, serão contidos as variáveis do PHP.
Contudo, para esse desafio não se sabe ao certo qual o processo relacionado à página gerada, então tentemos outra solução.

Ao utilizar como PATH, no lugar de `/proc/NUMERO_DO_PROCESSO_PHP/`, utilizemos `/dev/fd/`, que também consegue acessar as variáveis dos ponteiros do PHP. Assim, ao usarmos:

`curl -X GET https://CTF.com/?include=/dev/fd/NUMERO`

e testarmos as possibilidades, encontramos a flag em '/dev/fd/10'
