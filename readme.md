# Faculdade de Tecnologia "José Crespo Gonzales" -- _FATEC_ Sorocaba -- _Centro Paula Souza_

## Método de Newton-Raphson

O presente projeto consiste na implementação do método de Newton-Raphson.
Este método tem por objetivo encontrar as raízes de uma determinada função. Mais
informações sobre o método em si podem ser encontradas **nesta página da Wikipedia**.

* Detalhes de Implementação
* Instalação
* Dependências
* Utilização


### Detalhes de Implementação

Para este projeto foi utilizada a linguagem de programação Python, mais
específicamente na versão 3.6. A base de código consiste basicamente em um 
agente de análise sintática, responsável por converter a representação textual
de uma expressão matemática em seus dados correspondentes; e nas classes que
abstraem (de modo simplista) os componentes de uma função matemática qualquer.

O programa é capaz de ler uma sequência válida de caracteres (como por exemplo:
`"-x^4+12x^3-8x^2-16x+4"`), construir os monômios -x<sup>4</sup>, +12x<sup>3</sup>,
-8x<sup>2</sup>, -16x e a constante +4 que compõem a função e, ao fim, construir a
função em si. Cada monônimo, variável ou constante é em si mesmo um objeto que
atende as duas funcionalidades interessantes ao método: execução do cálculo e derivação.

Todos os objetos criados a partir da sequência de caracteres obedecem às regras de
derivação, contudo, apenas polinômios (de qualquer grau) têm suporte. Funções
logarítmicas, exponenciais, trigonométricas ainda não são suportadas.


### Instalação

Programas desenvolvidos na linguagem de programação Python dependem de um interpretador,
já que suas instruções não são convertidas em código-máquina, mas interpretadas durante
a execução. Por outro lado, o desenvolvimento é consideravelmente mais prático e rápido.
Este projeto requer a instalação prévia do interpretador em qualquer versão igual ou
superior à 3.6.

[Link para a página de download do instalador.](https://www.python.org/downloads/release/python-365/)

Após a instalação, arquivos de texto com a extensão `*.py` ou `*.pyw` serão
associados ao interpretador e considerados scripts ou programas escritos em Python.

O arquivo ZIP contendo o programa do projeto, disponível **neste link**, não requer
descompactação. O programa pode ser executado a partir da pasta na qual foi colocado.


### Dependências

Este projeto não depende de nenhuma biblioteca ou programa adicional.


### Utilização

Não possuindo interface gráfica de usuário, este projeto deve ser acionado via linha
de comando:

```
python c:\downloads\newton.zip "-x^4+12x^3-8x^2-16x+4;" k=100000 x=1 e=0.00001
```

O exemplo acima supõe que o interpretador esteja corretamente instalado, o que permite
o seu acionamento no prompt através do comando `python` em qualquer diretório do sistema.
A seguir, o endereço `c:\downloads\newton.zip` corresponde hipoteticamente ao local do
programa deste projeto, que será interpretado. Os argumentos que seguem são enviados ao
programa (não ao interpretador) para seu devido processamento.

#### Execução direta ou por lote

O programa pode processar uma função em particular com seus argumentos ou pode executar
de uma só vez uma sequência de funções usando os mesmos argumentos ou argumentos específicos.
Considere o seguinte como o conteúdo de um arquivo de texto, nomeado `entrada.txt`:
 
```
-3x+2 x=2 k=5 e=1 verbose
4x^2-3x+2 x=2 k=5 e=0.0001
5x^3+4x^2-3x+2 x=2 k=5 e=0.01
default verbose e=0.0001
-3x+2 x=2 k=25
4x^2-3x+2 x=2 k=100
5x^3+4x^2-3x+2 x=2 k=100 e=0.00001
```

Para as linhas 1 a 3 e 5 a 7 vê-se a função a ser processada e os argumentos para
cada função: `k` para máximo de iterações, `e` para Erro (ou [Épsilon](https://pt.wikipedia.org/wiki/E)) e `x` para valor
inicial de X. Há a opção `verbose`, que imprime o resultado da execução de maneira mais
legível, porém mais extensa.

A linha 4 define argumentos _default_ para as funções subsequentes. No exemplo acima, todas
as funções a partir da linha 5 terão `e` como default `0.0001`, caso este argumento seja
omitido. Além disso, `verbose` será aplicado a todas as linhas.

A partir deste arquivo, o programa poderá ser acionado da seguinte maneira:
```
python c:\downloads\newton.zip c:\entrada.txt
```
As funções serão processadas e o resultado será impresso no prompt de comando. Contudo, é possível especificar um arquivo de texto para a impressão do resultado:

```
python c:\downloads\newton.zip c:\entrada.txt c:\saida.txt
```
Com a adição de `c:\saida.txt`, o resultado será salvo no arquivo especificado, sobrescrevendo qualquer conteúdo anterior à execução.
