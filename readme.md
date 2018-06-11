# Fatec Sorocaba "José Crespo Gonzalez" - _CENTRO PAULA SOUZA_ 

## Cálculo Diferencial - Implementação do Método de Newton

Este projeto, como o nome sugere, é a implementação na linguagem de programação
[Python](https://www.python.org) (na versão 3.6.x) do [Método de Newton-Raphson](https://pt.wikipedia.org/wiki/Método_de_Newton-Raphson),
que tem por objetivo estimar as raíses (zeros) de uma função.

### Características

O ciclo de vida segue a estrutura básica de um programa executado por [linha de comando](https://pt.wikipedia.org/wiki/Interface_de_linha_de_comandos):
receber os tipos de argumentos de entrada expecificados abaixo, efetuar os cálculos, e imprimir os resultados ao término.

#### Entrada como arquivo de texto

O programa pode ser acionado com a seguinte linha no prompt de comando:

````
python newton.zip entrada.txt saida.txt
````

O exemplo acima assume que os arquivos `newton.zip`, `entrada.txt` e `saida.txt` estão na pasta atual onde o comando
será executado, caso contrário, o caminho absoluto de cada arquivo deve ser fornecido.

##### Formato do arquivo de entrada

O arquivo de entrada contém uma lista de funções, uma por linha, que serão calculadas pelo programa para produzir o
resultado desejado. Abaixo está um exemplo de arquivo de entrada em formato [CSV](https://pt.wikipedia.org/wiki/Comma-separated-values):

````
f(x)=-5x^3 +2x^2 -x +1, x=3.5, i=100, e=0.01
g(x)=(3x^2 -5)/(x^2 + 3), x=-4, i=1000, e=0.005
f(x)=x^2 -2x +4, x=-10, i=10000, e=0.0001
````

Que corresponde a

| Função                     | x<sub>0</sub> | i<sub>max</sub>      | [E][2]       |
|:--------------------------:|:-------------:|:--------------------:|:------------:|
| `f(x)=-5x^3 +2x^2 -x +1`   | x=`3.5`       | i=`100`              | e=`0.01`     |
| `g(x)=(3x^2 -5)/(x^2 + 3)` | x=`-4`        | i=`1000`             | e=`0.005`    |
| `f(x)=x^2 -2x +4`          | x=`-10`       | i=`10000`            | e=`0.0001`   |

#### Entrada como valor imediato

Como forma opcional de execução, é possível fornecer um único caso teste direto na linha de comando:

```
python newton.zip f=f(x)=x^2-2x+4 x=3.5 i=100 e=0.01
```

> **Atenção**: note que, neste caso, cada argumento é separado por um espaço, que tem esta _única_ finalidade.

#### Processamento da entrada

A execução do programa se dá, inicialmente, pela análise sintática dos argumentos. Os
componentes do cálculo são daí inicializados e então o cálculo é efetuado. Em caso de
erros ou indeterminações (divisão por zero), o programa é encerrado imediatamente e a
mensagem de erro correspondente é impressa no prompt de commando.

#### Impressão do resultado

O resultado será impresso no prompt de comando para execução com entrada imediata, bem
como na entrada por meio de arquivo de texto caso não seja especificado um arquivo para
a impressão do resultado. Caso um arquivo de saída seja especificado, qualquer dado anterior
à execução será perdido e os novos resultados serão gravados.

##### Formato do resultado

Para impressão no prompt de comando, o formato do resultado segue um padrão mais verboso
e descritivo (os valores abaixo são ilustrativos):

```
RESULTADO DE f(x)=3x^2+x-1; x=0.5 (1000 iterações, épsilon em 0.001)
--------------------------------------------------------------------
            Nº de iterações: 789
Valor de x na 789ª iteração: 0.999999
       Valor de f(0.999999): 0.0009998
```

Para impressão em arquivo de saída, o formato do resultado é mais compacto, em CSV,
similar ao arquivo de entrada, com dados extra:

```
f(x)=-5x^3 +2x^2 -x +1, x=3.5, iMAX=100, e=0.01, i=97, iX=0.8830, fX=0.009
g(x)=(3x^2 -5)/(x^2 + 3), x=-4, iMAX=1000, e=0.005, i=883, iX=0.9, fX=0.001
f(x)=x^2 -2x +4, x=-10, iMAX=10000, e=0.0001, i=7384, iX=-3.001, fX=0.00003
```

Similar a:

| Função                     | x<sub>0</sub> | i<sub>max</sub>      | [E][2]       | i            | x<sub>i</sub> | f(x<sub>i</sub>) |
|:--------------------------:|:-------------:|:--------------------:|:------------:|:------------:|:-------------:|:----------------:|
| `f(x)=-5x^3 +2x^2 -x +1`   | x=`3.5`       | i=`100`              | e=`0.01`     | i=`0.01`     | Xi=`0.01`     | Fx=`0.01`        |
| `g(x)=(3x^2 -5)/(x^2 + 3)` | x=`-4`        | i=`1000`             | e=`0.005`    | i=`0.005`    | Xi=`0.005`    | Fx=`0.005`       |
| `f(x)=x^2 -2x +4`          | x=`-10`       | i=`10000`            | e=`0.0001`   | i=`0.0001`   | Xi=`0.0001`   | Fx=`0.0001`      |
| `f(x)=x^2 -2x +4`          | x=`-10`       | i=`10000`            | e=`0.0001`   | i=`0.0001`   | Xi=`0.0001`   | Fx=`0.0001`      |


### Síntaxe

Segue abaixo as regras básicas de síntaxe para a definição de funções.

#### Numerais

Valores inteiros e reais são suportados. Números reais usam o ponto (`.`, não `,`)
para separar as casas decimais. Exemplos:
```
REAIS VÁLIDOS:
0.0     3.     .301       0.0001     102103.2

INTEIROS VÁLIDOS:
000     3      006001     10346703
```

#### Literais

Qualquer letra minúscula do alfabeto (`a-z`) será interpretada como literal. Um
literal será sempre composto de uma única letra. Letras maiúsculas têm outra 
finalidade, descrita abaixo. 

#### Operadores

Os operadores `+` e `-` atuam de modo unário (sinal) e binário (adição e subtração). Para
multiplicação, `*` é usado; e na divisão, `/`. Expoentes devem estar precedidos
por `^` e, para funções exponenciais ou expoentes negativos, o expoente deve
estar delimitado por parênteses. Raíses podem ser declaradas de duas maneiras, mas
ambas usam a letra `V` como operador. Exemplos:

| Operador         | Símbolo  | Exemplo                         |
|:----------------:|:--------:|:-------------------------------:|
| Sinal positivo   | `+`      | `+100` ou `3t `                 |
| Sinal negativo   | `-`      | `-x`                            |
| Adição           | `+`      | `4+3x`                          |
| Subtração        | `-`      | `x-5`                           |
| Multiplicação    | `*`      | `4x*E`                          |
| Divisão          | `/`      | `Pi/2`                          |
| Exponenciação    | `^`      | `x^4` ou `E^(x^2)` ou `2x^(-1)` |
| Radiciação       | `V`      | `'3V27'`, `V5x'` ou `V(3_5x^4)` |

> Note que, nos exemplos de radiciação, o apóstrofo `'` serve para delimitar o
> índice (quando diferente de 2) e o radicando (quando a expressão for simples).
> Na segunda forma, de função, o índice e o radicando são delimitados por parênteses
> e separados entre si por `_`.  

#### Constantes Literais

Para constantes literais, `Pi`, `Tau` e `E` estão disponíveis. A tabela
abaixo mostra a precisão utilizada.

| `Pi`              | `Tau`             | `E`               |
|:-----------------:|:-----------------:|:-----------------:|
| 3.141592653589793 | 6.283185307179586 | 2.718281828459045 |


#### Funções

Para funções, a síntaxe segue -- como o nome descreve, o padrão de função. Por esta
razão, elas podem ser utilizadas como parte literal (ex.: `3Ln(x)^2` = `3*(Ln(x))^2`)

As funções
disponíveis são:

| Função            | Símbolo | Exemplo           |
|:-----------------:|:-------:|:-----------------:|
| Logarítmo         | `Log`   | `Log(x)`, `Log(2_32)` |
| Logarítmo Natural | `Ln`    | `Ln(x)`, `Ln(E)` |
| Cosseno           | `Cos`   | `Cos(45)`, `Cos(3x)^2` |
| Seno              | `Sen`   | `Sen(3x+2)` |
| Tangente          | `Tg`    | `Tg(1/x)` |
| Secante           | `Sec`   | `Pi*Sec(180)` |
| Cossecante        | `CoSec` | `CoSec(x-1)` |
| Cotangente        | `CoTg`  | `2CoTg(Vx')` |

> **Atenção**: Para `Log(x)`, a base padrão é 10. Assim como em radicais, a base e o
> logaritmando devem estar separados por `_`.

#### Delimitadores

Parênteses `()` e colchetes `[]` podem ser utilizados como delimitadores. É importante
notar que expressões delimitadas adjacentes (ex.: `(2x+1)(2x-1)`) não são interpretadas como
multiplicação; o operador `*` _deve_ estar presente (também por questão de simetria com o operador `/`).

Espaços em branco são suportados apenas fora do contexto da execução, isto é,
durante a análise sintática. O prompt de comando, por definição, considera espaços
como separadores de argumentos, portanto, algo como `f(x)=32x^2 +5x -2` será recebido
não como um polinômio, mas como 3 elementos: `f(x)=32x^2`, `+5x` e `-3`. Por este
motivo, é melhor evitar espaços em braco.

[1]: https://pt.wikipedia.org
[2]: https://pt.wikipedia.org