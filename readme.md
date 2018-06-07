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

| Função                    | Valor inicial | Nº de [iterações][1] | [Epsilon][2] |
|:-------------------------:|:-------------:|:--------------------:|:------------:|
| f(x)=-5x^3 +2x^2 -x +1    | x=3.5         | i=100                | e=0.01       |
| g(x)=(3x^2 -5)/(x^2 + 3)  | x=-4          | i=1000               | e=0.005      |
|f(x)=x^2 -2x +4            | x=-10         | i=10000              | e=0.0001     |

#### Entrada como valor imediato

Como forma opcional de execução, é possível fornecer um único caso teste direto na linha de comando:

python newton.zip f=f(x)=x^2-2x+4 x=3.5 i=100 e=0.01

> Cuidado: neste caso, cada argumento é separado por um espaço, que tem esta _única_ finalidade.

[1]: https://pt.wikipedia.org
[2]: https://pt.wikipedia.org