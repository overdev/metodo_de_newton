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

import math
from typing import Any, Optional, Union, Iterable


def clsname(obj) -> str:
    """Função auxiliar que retorna o nome da classe do objeto dado."""
    return obj.__class__.__qualname__


def signal(value: Union[int, float]) -> str:
    """Retorna o sinal (textual) do valor `value`."""
    return '-' if value < 0 else '+'


class EvaluationError(Exception):
    """Excessão lançada em obj.evaluate(**kwargs) na ocorrência de algum erro."""
    pass


class DerivationError(Exception):
    """Excessão lançada em obj.derive() na ocorrência de algum erro."""
    pass


class Base:
    """Classe Base.

    Define a interface comum entre todos os objetos de tipo valor, operador e função.
    """

    @classmethod
    def parse(cls, expr: str, start: int=0, stop: int=-1) -> 'Base':
        """Cria e retorna uma nova instância do objeto a partir da análize léxica/sintática da expressão `expr`.

        `expr`: expressão a ser analisada.
        `start`: posição inicial (opcional) a partir de onde a análise deve começar.
        `stop`: posição final (opcional) onde a análise terminará.

        Deve ser implementada na subclasse.
        """
        raise NotImplementedError(f"Not implemented by {cls.__name__}.")

    def __str__(self) -> str:
        """Retorna a representação textual do objeto."""
        return clsname(self)

    def derive(self) -> 'Base':
        """Calcula e retorna a taxa de variação instantânea deste objeto.

        Deve ser implementado na subclasse.
        """
        raise NotImplementedError(f"Not implemented by {clsname(self)}.")

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Calcula e retorna o valor deste objeto.

        `kwargs` aplicará a substituição de qualquer literal pelo valor constante correspondente.

        Deve ser implementado na subclasse.
        """
        raise NotImplementedError(f"Not implemented by {clsname(self)}.")

    def multiply(self, other: 'Base') -> 'Base':
        """Realiza a multiplicação deste fator com o fator `other` à direita.

        O tipo de objeto retornado depende dos tipos dos fatores. Apenas valores constantes
        poderão ser computados. Por exemplo, a constante 3 multiplicada pelo literal x deve
        resultar no monômio 3x; e não no resultado computado de 3 * x, que requer uma constante
        para substituir x.

        Deve ser implementado na subclasse.
        """
        raise NotImplementedError(f"Not implemented by {clsname(self)}")


class Constant(Base):
    """Classe de valor Constante.

    Representa um valor numérico qualquer (real ou inteiro).
    """

    @classmethod
    def parse(cls, expr: str, start: int=0, stop: int=-1) -> 'Constant':
        """Implementação de Base.parse(expr[, start[, stop]]).

        Aceita como entrada válida um sequência de digitos 0~9, separada opcionalmente por 1 ponto
        decimal (".").
        """
        pass

    def __init__(self, value: Union[int, float]=0) -> None:
        """Inicialização do objeto."""
        self._value: Union[int, float] = value

    def __str__(self) -> str:
        """Implementação de Base.__str__()."""
        sign = '+' if self._value >= 0 else ''
        return f"{sign}{self._value}"

    @property
    def signal(self) -> int:
        """Retorna -1 se a constante for negativa, 1 caso contrário."""
        return -1 if self._value < 0 else 1

    def derive(self) -> 'Constant':
        """Implementação de Base.derive()."""
        return Constant(0)

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Implementação de Base.evaluate().

        Detalhe: retorna o valor desta contante. Argumentos em `kwargs` são ignorados.
        """
        return self._value

    def multiply(self, other: Base) -> Base:
        """Implementação de Base.multiply(other)."""
        if isinstance(other, Constant):
            # valores constantes podem ser computados.
            return Constant(self._value * other.evaluate())

        elif isinstance(other, Literal):
            # compõe um monômio
            # return Monomial(Constant(self._value), Power(Literal(other.name), Constant(1)))
            pass

        elif isinstance(other, Expr):
            # multiplica este fator a cada termo da expressão `other`.
            # TODO: chamar expr.simplify() para simplificar a espressão caso possível.
            return Expr(self.multiply(t) for t in other.terms)


class Literal(Base):
    """Classe de valor variável, Literal.

    Representa um nome (letra) substituível por um valor constante durante o cálculo.
    """

    @classmethod
    def parse(cls, expr: str, start: int=0, stop: int=-1) -> 'Literal':
        """Implementação de Base.parse(expr[, start[, stop]]).

        Aceita como entrada válida um único caractére alfabético minúsculo.
        """
        pass

    def __init__(self, name: str) -> None:
        """Inicialização do objeto."""
        self._name: str = name

    def __str__(self) -> str:
        """Implementação de Base.__str__()."""
        return f"{self._name}"

    @property
    def name(self) -> str:
        """Retorna o nome deste Literal."""
        return self._name

    def derive(self) -> Constant:
        """Implementação de Base.derive()."""
        return Constant(1)

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Implementação de Base.evaluate().

        Detalhe: requer o nome deste objeto como argumento-chave em `kwargs`
        para substituição do valor.
        """
        if self._name not in kwargs:
            raise EvaluationError(f"'{self._name}' requerido mas não encontrado nos argumentos-chave.")
        return kwargs.get(self._name, 1)


class Expr(Base):
    """Classe de operação, Expr.

    Representa uma expressão, isto é, sequência de termos (ex.: -3 +x +5x, (-1)),
    geralmente cercados por parênteses.
    """

    @classmethod
    def parse(cls, expr: str, start: int=0, stop: int=-1) -> 'Literal':
        """Implementação de Base.parse(expr[, start[, stop]]).

        Aceita como entrada válida os caractéres '(', '[', ')' e ']'.
        """
        pass

    def __init__(self, *terms) -> None:
        """Inicialização do objeto."""
        self._terms: list = list(terms)

    def __str__(self) -> str:
        """Implementação de Base.__str__()."""
        exp = ' '.join([str(t) for t in self._terms])
        return f'({exp})'

    @property
    def terms(self) -> Iterable[Base]:
        """Retorna um iterador para os termos desta expressão."""
        return self._terms.__iter__()

    def derive(self) -> 'Expr':
        """Implementação de Base.derive()."""
        return Expr(t.derive() for t in self._terms)

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Implementação de Base.evaluate().

        Detalhe: passará os argumentos chaves para os termos componentes, que poderão ser
        requeridos.
        """
        return sum([t.evaluate(**kwargs) for t in self._terms])

    def multiply(self, other) -> 'Expr':
        pass


class Monomial(Base):
    """Classe de valor, Monomial.

    Representa um monômio (ex.: 3x, -5x^2, -x^3). Por padrão, todo monômio
    contém um expoente constante (1) e uma base constante (1)
    """

    @classmethod
    def parse(self, expr: str, start: int=0, stop: int=-1) -> 'Monomial':
        """Implementação de Base.parse(expr[, start[, stop]])"""
        pass

    def __init__(self, liter: Literal, const: Optional[Constant]=None, expon: Optional[Base]=None) -> None:
        """Inicialização do objeto."""
        self._constant = Constant(const.evaluate()) if isinstance(const, Constant) else Constant(1)
        exp = Constant(1) if expon is None else expon
        # self._power = Power(Literal(liter.name), exp)

    def __str__(self) -> str:
        """Implementação de Base.__str__()."""
        k = signal(self._constant.evaluate()) if self._constant.evaluate() != 1 else str(self._constant)
        return ''


class Sign(Base):
    """Classe de operação, Sign.

    Representa o signal de uma função, para casos em que o sinal não é explícito, como,
    por exemplo, a subtração de duas funções (na derivada que faz uso da regra do quociente).
    """

    def __init__(self, negative: bool, obj: Base) -> None:
        self._negative: bool = negative
        self._obj: Base = obj

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Implementação de Base.evaluate()."""
        value = self._obj.evaluate(**kwargs)
        if self._negative:
            return -value
        return value


class Product(Base):
    """Classe de operação, Product.

    Representa a multiplicação de dois fatores.
    """

    def __init__(self, left: Base, right: Base) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{self._left}*{self._right}"

    def derive(self) -> Expr:
        """Implementação de Base.derive().

        Detalhe: y' = f'(x)*g(x) + f(x)*g'(x); y' é uma expressão: sendo esq = f(x) e dir = g(x), então
        y = Expr(Product(esq.derive(), dir), Product(esq, dir.derive()))
        """

        return Expr(Product(self._left.derive(), self._right), Product(self._left, self._right.derive()))


class Quotient(Base):

    def __init__(self, numerator: Base, denominator: Base) -> None:
        self._numerator = numerator
        self._denominator = denominator

    def __str__(self) -> str:
        return f"{self._numerator}/{self._denominator}"


class Power(Base):

    def __init__(self, base: Base, exponent: Base) -> None:
        self._base = base
        self._exponent = exponent

    def __str__(self) -> str:
        e = str(self._exponent)
        if e.startswith('-'):
            exp = f"({e})"
        elif e.startswith('+'):
            exp = e[1:]
        else:
            exp = e
        return f"{self._base}^{exp}"

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Implementação de Base.evaluate(**kwargs)"""
        return self._base.evaluate(**kwargs) ** self._exponent.evaluate(**kwargs)


class Radical(Base):

    def __init__(self, index: Constant, radicand: Base) -> None:
        self._index = index
        self._radicand = radicand

    def __str__(self) -> str:
        i = str(self._index)
        if i.startswith('-') or i.startswith('+'):
            ind = i[1:]
        else:
            ind = i
        return f"'{ind}V{self._radicand}'"

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Implementação de Base.evaluate(**kwargs)"""
        pass


class Log2(Base):

    def __init__(self, logaritm: Base) -> None:
        self._logaritm = logaritm


class Log10(Base):

    def __init__(self, logaritm: Base) -> None:
        self._logaritm = logaritm


class LogN(Base):

    def __init__(self, logaritm: Base) -> None:
        self._logaritm = logaritm


class Cos(Base):

    def __init__(self, value: Base) -> None:
        self._value = value


class Sin(Base):

    def __init__(self, value: Base) -> None:
        self._value = value


class Tan(Base):

    def __init__(self, value: Base) -> None:
        self._value = value


if __name__ == '__main__':
    c = Constant(5)
    x = Literal('x')
    exp = Expr(Constant(3), Constant(-5), Constant(7))
    pwr = Power(Constant(4), Literal('x'))
    rad = Radical(Constant(2), Constant(9))
    print(c, x, exp, pwr, rad)
