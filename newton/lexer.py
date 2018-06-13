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

from enum import Enum
from typing import List, Union, Optional
import classes2

__all__ = [
    'TKind',
    'Token',
    'Lexer',
]

SENTINEL = object()


END = ('\n',)
WHITESPACE = (' ',)
LIGATURE = ('_',':')
NUMBERS = tuple('1234567890')
LETTERS = tuple('abcdefghijklmnopqrstuvwxyz')
OPERATORS = tuple('+-*/^')
GROUPS = tuple("([])")
FNLETTERS = tuple('PEVLCST')
FUNCTIONS = 'Pi', 'Tau', 'E', 'V', 'Log', 'Ln', 'Cos', 'Sen', 'Tg', 'Sec', 'CoSec', 'CoTg'


class TKind(Enum):
    NONE = 0
    NUMBER = 1
    LITERAL = 2
    OPERATOR = 3
    PI = 4
    TAU = 5
    E = 6
    RADICAL = 7
    LOG = 8
    LN = 9
    COS = 10
    SEN = 11
    TG = 12
    SEC = 13
    COSEC = 14
    COTG = 15
    LIGATURE = 16
    GROUP_BEGIN = 17
    GROUP_END = 18


class Token:
    """Classe Token.

    Representa um componente de uma expressão, por exemplo, um numeral, um operador,
    um símbolo, etc.
    """

    def __init__(self, kind: TKind, value: str, index: int) -> None:
        self.kind = kind
        self.value = value
        self.index = index

    def __repr__(self) -> str:
        return f"({self.kind.name}: '{self.value}' @{self.index})"

    __str__ = __repr__


class Lexer:
    """Classe Lexer.

    Realiza a análise sintática da expressão fornecida e produz uma sequência
    de tokens correspondente aos componentes da expressão.
    """

    def __init__(self):
        self._stack: List[str] = []
        self._expression: str = ''
        self._errors: List[str] = []
        self._tokens: List[Token] = []

    @property
    def tokens(self):
        return self._tokens

    def quit(self) -> None:
        for err in self._errors:
            print(err)
        quit(-1)

    def tokenize(self, expression: str) -> bool:
        """Efetua a análise da expressão `expression`."""
        index: int = 0
        start: int = 0
        char: str = ''
        value: str = ''
        kind: TKind = TKind.NONE
        def ch():
            #global index
            try:
                return expression[index]
            except IndexError:
                return '\n'

        def match(*values) -> bool:
            # global char
            n = len(values)
            if n == 0:
                return False
            elif n == 1:
                return char == values[0]
            else:
                return char in values

        def expect(*values, msg: str="{} experado, {} encontrado.") -> bool:
            # global char
            n = len(values)
            if n == 0:
                return False
            elif n == 1:
                if not match(*values):
                    self._errors.append(msg.format(values[0], char))
                    return False
            else:
                if not match(*values):
                    self._errors.append(msg.format(' ou '.join(values), char))
                    return False
            return True

        def push():
            global value
            self._stack.append(value)
            value = ''

        def pop():
            global value
            value = self._stack.pop()

        def save(t: Token):
            global value
            self._tokens.append(t)

        i = 0
        while index < len(expression):

            char = ch()

            if match(*NUMBERS) or match('.'):
                dec = char == '.'
                num = char != '.'
                if kind is not TKind.NUMBER and kind is not TKind.NONE:
                    save(Token(kind, value, start))
                start = index
                value = char
                kind = TKind.NUMBER
                index += 1
                char = ch()
                if match('.'):
                    if dec:
                        self._errors.append('Ponto decimal inexperado em \'{}\''.format(expression[start:]))
                        self.quit()
                    dec = True
                    value += char
                    index += 1
                    char = ch()
                    if not num and not expect(*NUMBERS):
                        self.quit()
                while match(*NUMBERS):
                    value += char
                    index += 1
                    char = ch()
                    if match('.'):
                        if dec:
                            self._errors.append('Ponto decimal inexperado em \'{}\''.format(expression[start:]))
                            self.quit()
                        dec = True
                        value += char
                        index += 1
                        char = ch()

            elif match(*LETTERS):
                if kind is not TKind.LITERAL and kind is not TKind.NONE:
                    save(Token(kind, value, start))
                save(Token(TKind.LITERAL, char, index))
                index += 1
                start = index
                kind = TKind.NONE

            elif match(*OPERATORS):
                if kind is not TKind.OPERATOR and kind is not TKind.NONE:
                    save(Token(kind, value, start))
                save(Token(TKind.OPERATOR, char, index))
                index += 1
                start = index
                kind = TKind.NONE

            elif match(*GROUPS):
                if kind not in (TKind.GROUP_BEGIN, TKind.GROUP_END) and kind is not TKind.NONE:
                    save(Token(kind, value, start))
                if char == '(' or char == '[':
                    save(Token(TKind.GROUP_BEGIN, char, start))
                elif char == ')' or char == ']':
                    save(Token(TKind.GROUP_END, char, start))
                index += 1
                start = index
                kind = TKind.NONE

            elif match(*FNLETTERS):
                if kind is not TKind.NONE:
                    save(Token(kind, value, start))
                start = index
                fn = expression[index:]
                if fn.startswith('Pi'):
                    save(Token(kind.PI, 'Pi', start))
                    index += 2
                elif fn.startswith('Tau'):
                    save(Token(kind.TAU, 'Tau', start))
                    index += 3
                elif fn.startswith('E'):
                    save(Token(kind.E, 'E', start))
                    index += 1
                elif fn.startswith('V'):
                    save(Token(kind.RADICAL, 'V', start))
                    index += 1
                elif fn.startswith('Log'):
                    save(Token(kind.LOG, 'Log', start))
                    index += 3
                elif fn.startswith('Ln'):
                    save(Token(kind.LN, 'Ln', start))
                    index += 2
                elif fn.startswith('Cos'):
                    save(Token(kind.COS, 'Cos', start))
                    index += 3
                elif fn.startswith('Sen'):
                    save(Token(kind.SEN, 'Sen', start))
                    index += 3
                elif fn.startswith('Tg'):
                    save(Token(kind.TG, 'Tg', start))
                    index += 2
                elif fn.startswith('Sec'):
                    save(Token(kind.SEC, 'Sec', start))
                    index += 2
                elif fn.startswith('CoSec'):
                    save(Token(kind.COSEC, 'CoSec', start))
                    index += 5
                elif fn.startswith('CoTg'):
                    save(Token(kind.COTG, 'CoTg', start))
                    index += 4
                else:
                    self._errors.append("Símbolo inválido: {}".format(fn))
                    self.quit()
                char = ch()
                start = index
                kind = TKind.NONE

            elif match(*LIGATURE):
                if kind is not TKind.LIGATURE and kind is not TKind.NONE:
                    save(Token(kind, value, start))
                save(Token(TKind.LIGATURE, char, index))
                index += 1
                start = index
                char = ch

            elif match(*END):
                save(Token(kind, value, start))
                return True

            else:
                print(char)
                return False

        else:
            if kind is not TKind.NONE:
                save(Token(kind, value, start))


class Parser:

    def __init__(self) -> None:
        self._index = 0
        self._tokens: List[Token] = []

    @property
    def token(self) -> Token:
        return self._tokens[self._index]

    def match(self, *value) -> bool:
        n = len(value)
        if n == 0:
            return False
        for v in value:
            if isinstance(v, TKind) and v is self.token.kind:
                return True
            elif isinstance(v, str) and v == self.token.value:
                return True
        return False

    def next(self) -> Union[Token, object]:
        self._index += 1
        if not 0 <= self._index < len(self._tokens):
            return SENTINEL
        return self._tokens[self._index]

    def expect(self, *value) -> None:
        n = len(value)
        if n == 0:
            print(f"{value} experado, {self.token} achado.")
            quit()
        elif not self.match(*value):
            print(f"{value} experado, {self.token} achado.")
            quit()
        self.next()

    def parse_constant(self) -> Optional[classes2.Constant]:
        positive = True
        if self.match('+', '-', TKind.NUMBER):
            if self.match('-'):
                positive = False
                self.next()

            if self.match(TKind.NUMBER):
                if '.' in self.token.value:
                    k = float(self.token.value)
                else:
                    k = int(self.token.value)
                self.next()
            else:
                k = 1
            return classes2.Constant(k if positive else -k)
        return None

    def parse_literal(self) -> Optional[classes2.Literal]:
        if self.match(TKind.LITERAL):
            x = self.token.value
            self.next()
            return classes2.Literal(x)
        return None

    def parse_radical(self) -> None:
        pass

    def parse_exponent(self) -> Union[classes2.Constant, classes2.FunctionABC]:
        ind = self._index
        close_brace = None
        if self.match('^'):
            self.next()
            if self.match('(', '['):
                close_brace = ')' if self.token.value == '(' else ']'
                self.next()

            e = self.parse_expr()

            if close_brace:
                self.expect(close_brace)
            return e

        else:
            print(f"'^' expected, got{self.token.kind}")

    def parse_expr(self) -> Optional[Union[classes2.Constant, classes2.FunctionABC]]:
        ind = self._index
        positive = True
        const = None
        liter = None
        func = None
        expon = None
        arg = None

        const = self.parse_constant()
        if self.match(TKind.LITERAL):
            liter = self.parse_literal()
        elif self.match(TKind.RADICAL):
            rad = self.parse_radical()

        if self.match('^'):
            expon = self.parse_exponent()




        return None



if __name__ == '__main__':
    lex = Lexer()
    lex.tokenize("(+.5x)^2/3.CoTg(5)^2+2*LnE")
    for t in lex.tokens:
        print(t)
