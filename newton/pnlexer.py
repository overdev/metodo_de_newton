# !/usr/bin/python
# -*- coding: utf-8 -*-

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# The MIT License (MIT)
#
# Copyright (c) 2018 Jorge A. Gomes (jorgegomes83 at hotmail dot com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from typing import Union, NamedTuple, List, Optional


__all__ = [
    'K',
    'X',
    'M',
    'F',
    'Scanner',
]


class K(NamedTuple):
    """Classe imutável K.

    Representa uma constante. O atributo `k`, que pode ser um número real ou inteiro,
    contém o valor desta constante.
    """
    k: Union[int, float]

    def __repr__(self):
        """Retorna a representação textual do construtor desta constante."""
        return f"K({self.k})"

    def __str__(self):
        """Retorna a representação textual desta constante."""
        return f"{self.k}" if self.k < 0 else f"+{self.k}"

    def derive(self) -> 'K':
        """Retorna a derivada desta constante, isto é, a constante 0."""
        return K(0)

    def eval(self, **kwargs) -> Union[int, float]:
        return self.k


class X(NamedTuple):
    """Classe imutável X.

    Representa uma variável. O atributo `x` contém o nome (uma letra) desta variável.
    """
    x: str

    def __repr__(self):
        """Retorna a representação textual do construtor deste literal."""
        return f"X('{self.x}')"

    def __str__(self):
        """Retorna a representação textual deste literal."""
        return f"{self.x}"

    def derive(self) -> 'K':
        """Retorna a derivada deste literal, isto é, a constante 1."""
        return K(1)

    def eval(self, **kwargs) -> Union[int, float]:
        """Calcula e retorna o valor deste literal, subtituindo todas o literal por uma constante."""
        if self.x not in kwargs:
            print(f"Valor de '{self.x}' não determinado.")
        return kwargs.get(self.x)


class M(NamedTuple):
    """Classe imutável M.

    Representa um monômio. O atributo `k` é uma constante, o atributo `x` é uma variável e
    o atributo `e` é o expoente (também uma constante).
    """
    k: K
    x: X
    e: K

    def __repr__(self):
        """Retorna a representação textual do construtor deste monômio."""
        return f"M({self.k},'{self.x}', {self.e})"

    def __str__(self):
        """Retorna a representação textual deste monômio."""
        if self.k.k == -1:
            k = '-'
        elif self.k.k == 1:
            k = '+'
        else:
            k = str(self.k)
        e = f"^{self.e}"
        if self.e.k == 1:
            e = ''
        elif self.e.k < 0:
            e = f"^({self.e})"
        else:
            n = str(self.e.k)
            if n.startswith('-'):
                n = n[1:]
            e = f"^{n}"

        return f"{k}{self.x}{e}"

    def derive(self) -> Union[K, X, 'M']:
        """Retorna a derivada deste monônimo, isto é, (e*k)x^(e-1)."""
        k = self.k.k
        e = self.e.k
        nk = e * k
        ne = e - 1
        if ne == 0:
            return self.k
        return M(K(nk), self.x, K(ne))

    def eval(self, **kwargs) -> Union[int, float]:
        """Calcula e retorna o valor deste monômio, subtituindo todas as variáveis."""
        k = self.k.eval(**kwargs)
        x = self.x.eval(**kwargs)
        e = self.e.eval(**kwargs)
        return k * (x ** e)


class F(NamedTuple):
    """Classe imutável F.

    Representa uma função polinomial."""
    ems: List[Union[M, K]]

    def __repr__(self):
        """Retorna a representação textual do construtor deste polinômio."""
        return f"F({repr(m) for m in self.ems})"

    def __str__(self):
        """Retorna a representação textual deste polinômio."""
        l = self.get_literals()
        n = len(l)
        if n == 0:
            args = ''
        elif n == 1:
            args = l[0]
        else:
            args = ', '.join(l)
        ems = ''.join([str(m) for m in self.ems])
        return f"{ems}"

    def get_literals(self) -> List[str]:
        literals = []
        for m in self.ems:
            if isinstance(m, M):
                if m.x.x not in literals and m.x.x != '':
                    literals.append(m.x.x)
        return literals

    def derive(self) -> 'F':
        """Retorna a derivada desta função."""
        return F([m.derive() for m in self.ems if isinstance(m, M)])

    def eval(self, **kwargs) -> Union[int, float]:
        """Calcula e retorna o valor desta função, subtituindo todas as variáveis."""
        return sum([m.eval(**kwargs) for m in self.ems])


class Scanner:
    """Classe auxiliar Scanner.

    É responsável por transformar uma sequência de caractéres representando
    uma função polinomial no objeto correspondente, que poderá ser processado
    por meio do Método de Newton.
    """

    def __init__(self, input_f: str):
        self._fs = input_f
        self._ind = 0
        self._monomials: List[Union[M, K]] = []
        self.k = ''
        self.x = ''
        self.e = ''

    def scan(self) -> Optional[F]:
        """Analisa a sequência de caractéres representando a função polinomial,
        gera e retorna a função executável correspondente.
        """
        empty = True
        i = 0
        while self.get() is not None:
            if i >= len(self._fs):
                print(f"unconditional loop.")
                quit()
            if empty:
                if self.match(*tuple('123456789.')):
                    self.scan_term()
                elif self.match(*tuple('abcdefghijklmnopqrstuvwxyz')):
                    self.k = '1'
                    self.x = self.get()
                    self.next()
                    if self.match('^'):
                        self.scan_e()
                    self.add()
                empty = False
            elif self.match('-', '+'):
                self.scan_term()
            elif self.match('_'):
                self.next()
            elif self.match(' ', ';'):
                break
            else:
                print(f"Caractére inexperado na posição {self._ind}: '{self.get()}'")
                quit()
            i += 1

        return F(self._monomials)

    def scan_term(self) -> None:
        """Analiza um termo da função e gera o monômio correspondente."""
        if self.match(*tuple('-+')):
            self.k = self.get()
            self.next()
            self.expect(*tuple('1234567890.abcdefghijklmnopqrstuvwxyz'))

        if self.match(*tuple('1234567890.')):
            self.scan_k()

        if self.match(*tuple('abcdefghijklmnopqrstuvwxyz')):
            self.x = self.get()
            self.next()
            self.expect('^', '+', '-', '_', ';')

        if self.match('^'):
            self.scan_e()

        self.add()

    def add(self) -> None:
        """Adiciona o último monônimo analisado à lista de termos da função."""
        k = self.to_value(self.k)
        e = self.to_value(self.e)
        if self.x == '':
            self._monomials.append(K(k**e))
        else:
            self._monomials.append(M(K(k), X(self.x), K(e)))
        self.k = ''
        self.x = ''
        self.e = ''

    def scan_k(self) -> None:
        """Analiza uma constante."""
        decimal = False
        while self.match(*tuple('1234567890.')):
            if self.match('.'):
                if not decimal:
                    decimal = True
                else:
                    print(f"Caractére inesperado: segundo ponto decimal na posição {self._ind}.")
                    quit()
            self.k += self.get()
            self.next()

    def scan_e(self, sym: bool=True) -> None:
        """Analiza um expoente constante"""
        decimal = False
        num = False
        end = None
        if sym:
            self.expect('^')
            self.next()
        if self.match('-'):
            print(f"Caractére inexperado ('-') na posição {self._ind}: expoente negativo deve estar cercado por parênteses.")
            quit()

        if self.match('('):
            self.next()
            end = ')'
            self.expect('-')
            self.e = '-'
            self.next()

        while self.match(*tuple('1234567890.')):
            if self.match('.'):
                if not decimal:
                    decimal = True
                else:
                    print(f"Caractére inesperado: segundo ponto decimal na posição {self._ind}.")
                    quit()
            else:
                num = True
            self.e += self.get()
            self.next()

        if not num:
            print(f"Nenhum dígito no expoente, na posição {self._ind}.")
            quit()

        if end is not None:
            self.expect(end)

    # region

    def to_value(self, string: str) -> Union[int, float]:
        """Converte uma representação textual de um numeral no objeto correspondente."""
        if string in ('', '-', '+'):
            if string == '-':
                return -1
            return 1
        if '.' in string:
            return float(string)
        else:
            if string.startswith('+'):
                return int(string[1:])
            return int(string)

    def get(self) -> Optional[str]:
        """Retorna o caractére atual a ser analizado."""
        if 0 <= self._ind < len(self._fs):
            return self._fs[self._ind]
        return None

    def match(self, *value) -> bool:
        """Retorna verdadeiro se caractére atual é igual ao valor ou um dos valores de `*value`.

        Falso, caso contrário.
        """
        return self.get() in value

    def next(self) -> None:
        """Avança o índicador de caractére para o caractére seguinte."""
        self._ind += 1

    def expect(self, *value) -> None:
        """Aborta a execução do scanner se o caractére atual não corresponder a um dos valores
        de `*value`.

        Uma mensagem de erro indicando o caractére esperado é impressa no prompt.
        """
        if not self.match(*value):
            if len(value) == 1:
                print(f"'{value[0]}' esperado, ao invés de {self.get()} na posição {self._ind}.")
            else:
                v = ', '.join([f"'{l}'" for l in value])
                print(f"{v} esperado, ao invés de '{self.get()}' na posição {self._ind}.")

            quit()

    # endregion
