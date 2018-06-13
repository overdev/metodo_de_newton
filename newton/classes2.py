
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
from typing import Union, List, Tuple

DEFAULT = (object(),)


def clsname(obj) -> str:
    """Função auxiliar que retorna o nome da classe do objeto dado."""
    return obj.__class__.__qualname__


def nroot(n: int, x: Union[int, float]) -> Union[int, float]:
    """Função auxiliar que retorna a raiz n-ésima de x."""
    if n <= 0:
        raise ValueError("Raíz de índice <= 0.")
    elif n == 1:
        return x
    elif n == 2:
        # return round(math.sqrt(abs(x)), 14)
        return math.sqrt(abs(x))
    else:
        # return round(math.pow(abs(x), 1 / n), 14)
        return math.pow(abs(x), 1 / n)


def signal(value: Union[int, float]) -> str:
    """Retorna o sinal (textual) do valor `value`."""
    return '-' if value < 0 else '+'


class FunctionABC:
    """Classe base abstrata FunctionABC.

    Define a interface comum para todas as possíveis funções deriváveis.
    """

    def __str__(self) -> str:
        """Representação textual da função."""
        return NotImplemented

    def __repr__(self) -> str:
        """Representação textual do construtor da função."""
        return f"{self.__class__.__qualname__}()"

    def __eq__(self, other) -> bool:
        """Compara esta função com a função `other` sob igualdade."""
        return self.__class__ is other.__class__

    def __ne__(self, other) -> bool:
        """Compara esta função com a função `other` sob diferença."""
        return self.__class__ is not other.__class__

    def copy(self) -> 'FunctionABC':
        """Retorna uma cópia desta função."""
        return NotImplemented

    def derive(self):
        """Retorna a derivada desta função."""
        return NotImplemented

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Calcula e retorna o resultado desta função."""
        return NotImplemented

    def tg_equation(self, **kwargs) -> 'FunctionABC':
        """Calcula e retorna a equação da reta tangente em x0."""
        df: FunctionABC = self.derive()
        m = df.evaluate(**kwargs)
        y0 = self.evaluate(**kwargs)
        return Sum(Product(Constant(m), Subtraction(Literal('x'), Literal('x0'))), Constant(y0))


class Constant:
    """Classe de função constante.

    Corresponde a `y = k`. Sua derivada é `y' = 0` e seu valor é `k`.
    """
    __slots__ = ('_k',)

    def __init__(self, k: Union[int, float]=1) -> None:
        self._k: Union[int, float] = k

    def __str__(self) -> str:
        """Retorna k, incluindo sinal."""
        return str(self._k)

    def __repr__(self) -> str:
        """Retorna a representação textual do contrutor desta função."""
        return f"{self.__class__.__qualname__}({self._k})"

    def __eq__(self, other):
        """Retorna verdadeiro se esta constante é igual à constante `other`. Falso, caso contrário."""
        return super(Constant, self).__eq__(other) and self._k == other.k

    def __ne__(self, other):
        """Retorna verdadeiro se esta constante é diferente de `other`. Falso, caso contrário."""
        if super(Constant, self).__eq__(other):
            return self._k != other.k
        return True

    @property
    def k(self) -> Union[int, float]:
        """Lê o valor de k."""
        return self._k

    def copy(self) -> 'Constant':
        """Retorna uma cópia desta constante."""
        return Constant(self._k)

    @staticmethod
    def derive() -> 'Constant':
        """Retorna a taxa de variação de `y = k`, que é `y' = 0`."""
        return Constant(0)

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor de k. Não realiza subtituição de literais."""
        return self._k + (len(kwargs) * 0)


class Literal:
    """Classe de função constante.

    Corresponde a `y = x`. Sua derivada é `y' = 1` e seu valor é `x`.
    """
    __slots__ = ('_name',)

    def __init__(self, name: str) -> None:
        self._name: str = name

    def __str__(self) -> str:
        """Retorna o literal."""
        return self._name

    def __repr__(self) -> str:
        """Retorna a representação textual do contrutor desta função."""
        return f"{self.__class__.__qualname__}('{self._name}')"

    def __eq__(self, other):
        """Retorna verdadeiro se esta constante é igual à constante `other`. Falso, caso contrário."""
        if super(Literal, self).__eq__(other):
            if self._name == other.name:
                return True
        return False

    def __ne__(self, other):
        """Retorna verdadeiro se esta constante é diferente de `other`. Falso, caso contrário."""
        if super(Literal, self).__eq__(other):
            if self._name != other.name:
                return True
        return False

    @property
    def name(self) -> str:
        """Lê o nome deste literal."""
        return self._name

    def copy(self) -> 'Literal':
        """Retorna uma cópia deste literal."""
        return Literal(self._name)

    def derive(self) -> 'Constant':
        """Retorna a taxa de variação de `y = x`, que é `y' = 1`."""
        return Constant(1)

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor de k. `kwargs` deve conter o nome deste literal."""
        if self._name not in kwargs:
            raise ValueError(f"'{self._name}' não encontrado em `kwargs`.")
        return kwargs.get(self._name, 1)


class Monomial(FunctionABC):
    """Classe de função com expoente constante.

    Corresponde a `y = k * x^n` ou `k = kx^n` em que `k` é uma constante, `x` é um literal
    e `e` é um inteiro.
    Sua derivada é `y' = k` e seu valor depende de `x`.
    """
    __slots__ = '_k', '_x', '_e'

    def __init__(self, x: Union['Literal', FunctionABC], e: Union['Constant', Tuple[object]]=DEFAULT,
                 k: Union['Constant', Tuple[object]]=DEFAULT) -> None:
        self._k: Constant = Constant(1) if k is DEFAULT else k
        self._e: Constant = Constant(1) if e is DEFAULT else e
        self._x: Literal = x

    def __str__(self) -> str:
        """Retorna a representação textual desta função."""
        x = str(self._x)
        e = f"^{self._e}"
        k = str(self._k)
        if self._k.k == 1:
            k = ''
        elif self._k.k == -1:
            k = '-'
        if self._e.k == 1:
            e = ''
        elif self._e.k == 0:
            e = ''
            x = ''
            k = str(self._k)if self._k.k >= 0 else f"({self._k})"
        elif self._e.k < 0:
            e = f"^({self._e})"
        return f"{k}{x}{e}"

    def __repr__(self) -> str:
        """Retorna a representação textual do contrutor desta função."""
        return f"{self.__class__.__qualname__}({self._x}, {self._e}, {self._k})"

    def __eq__(self, other):
        """Retorna verdadeiro se esta função é igual à constante `other`. Falso, caso contrário."""
        if super(Monomial, self).__eq__(other):
            if self._k == other.k and self._x == other.x and self._e == other.e:
                return True
        return False

    def __ne__(self, other):
        """Retorna verdadeiro se esta função é diferente de `other`. Falso, caso contrário."""
        if super(Monomial, self).__eq__(other):
            if self._k != other.k or self._x != other.x or self._e != other.e:
                return True
        return False

    @property
    def k(self) -> Constant:
        """Lê a constante desta função."""
        return self._k

    @property
    def x(self) -> Literal:
        """Lê o literal desta função"""
        return self._x

    @property
    def e(self) -> Constant:
        """Lê o expoente desta função"""
        return self._e

    def copy(self) -> 'Monomial':
        """Retorna uma cópia deste monômio."""
        return Monomial(self._x.copy(), self._e.copy(), self._k.copy())

    def derive(self) -> Union['Constant', 'Monomial']:
        """Retorna a taxa de variação de `y = kx`, que é `y' = k`."""
        k = self._k
        x = self._x
        e = self._e
        if e.k == 1:
            return Constant(k.k)
        return Monomial(x.copy(), Constant(e.k - 1), Constant(k.k * e.k))

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor de `kx`. `kwargs` deve conter o nome deste literal."""
        k = self._k
        x = self._x
        e = self._e
        return k.evaluate(**kwargs) * (x.evaluate(**kwargs) ** e.evaluate(**kwargs))


class Polinomial(FunctionABC):
    """Class de função polinomial.

    Representa uma sequência de dois ou mais monônios do tipo `kx^n`.

    A derivada de um polinômio corresponde à derivada de cada monômio componente.
    O valor deste polinimio depende do valor de todos os literais na função.
    """

    def __init__(self, *p) -> None:
        self._p: List[Monomial] = list(p)

    def __str__(self) -> str:
        """Retorna a representação textual deste polinômio"""
        f = ""
        for m in self._p:
            if isinstance(m, Monomial):
                k = '' if m.k.k < 0 else '+'
            elif isinstance(m, Constant):
                k = '' if m.k < 0 else '+'
            s = f"{k}{m}"
            f += s
        return f

    def derive(self) -> Union[Constant, Monomial, 'Polinomial']:
        """Retorna a taxa de variação deste polinômio."""
        df = []
        for m in self._p:
            dm: Union[Monomial, Constant] = m.derive()
            if isinstance(dm, Constant) and dm.k == 0:
                continue
            df.append(dm)
        if len(df) == 0:
            return Constant(0)
        elif len(df) == 1:
            return df[0]
        else:
            return Polinomial(*df)

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor deste polinomial. `kwargs` deve conter o nome de todos os literais."""
        return sum([m.evaluate(**kwargs) for m in self._p])


class Exponent(FunctionABC):
    """Classe de função exponencial.

    Corresponde a `y = u^v` em que a base `u` e o expoente `v` são funções,
    ou `y = b^n` em que a base `b` é uma constante ou literal e o expoente `n` é uma constante.
    Sua derivada é `y' = u^v * v'`, ou `y' = n*b^(n-1)` e seu valor depende da base e do expoente.
    """
    __slots__ = '_u', '_v'

    def __init__(self, u, v: Union[Constant, Literal, FunctionABC]) -> None:
        self._u: Union[Constant, Literal, FunctionABC] = u
        self._v: Union[Constant, Literal, FunctionABC] = v

    def __str__(self) -> str:
        """Retorna a representação textual desta função."""
        if self.is_exponential:
            if isinstance(self._u, FunctionABC):
                return f"({self._u})^({self._v})"
            else:
                return f"{self._u}^({self._v})"
        elif isinstance(self._u, FunctionABC):
            return f"({self._u})^{self._v}"
        return f"{self._u}^{self._v}"

    def __repr__(self) -> str:
        """Retorna a representação textual do contrutor desta função."""
        return f"{self.__class__.__qualname__}({self._u}, {self._v})"

    def __eq__(self, other):
        """Retorna verdadeiro se esta função é igual à constante `other`. Falso, caso contrário."""
        if super(Exponent, self).__eq__(other):
            if self._u == other.u and self._v == other.e:
                return True
        return False

    def __ne__(self, other):
        """Retorna verdadeiro se esta função é diferente de `other`. Falso, caso contrário."""
        if super(Exponent, self).__eq__(other):
            if self._u != other.u or self._v != other.e:
                return True
        return False

    @property
    def u(self) -> Union[Constant, Literal, FunctionABC]:
        """Lê a base desta função."""
        return self._u

    @property
    def v(self) -> Union[FunctionABC, Constant, Literal]:
        """Lê o expoente desta função"""
        return self._v

    @property
    def is_exponential(self) -> bool:
        """Retorna verdadeiro caso o expoente seja uma função, e Falso caso contrário."""
        return isinstance(self._v, (Literal, FunctionABC))

    def copy(self) -> 'Exponent':
        """Retorna uma cópia desta potência."""
        return Exponent(self._u.copy(), self._v.copy())

    def derive(self) -> Union[Constant, FunctionABC]:
        """Retorna a taxa de variação de `y = b^n`, que é `y' = n*b^(n-1)`."""
        if self.is_exponential:
            return Product(self._v.derive(), self._u.derive())

        elif isinstance(self._u, Constant):
            return Constant(1)

        elif isinstance(self._u, Literal):
            ek: int = self._v.k
            return Monomial(self._u.copy(), Constant(ek - 1), Constant(ek))

        elif isinstance(self._u, FunctionABC):
            ek: int = self._v.k
            return Monomial(self._u.copy(), Constant(ek - 1), Constant(ek))

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor desta função. A base pode depender de `kwargs`."""
        u = self._u.evaluate(**kwargs)
        v = self._v.evaluate(**kwargs)
        if u == 0 and v < 0:
            return float('+inf')
        return u ** v


class Sum(FunctionABC):
    """Classe de função soma.

        Representa a soma entre duas funções `u` e `v.
        Para `y = u + v` a derivada é `y' = u' + v'`.
        O valor desta função depende de ambos os termos.
        """

    __slots__ = '_a', '_b'

    def __init__(self, a: Union[Constant, FunctionABC], b: Union[Constant, FunctionABC]) -> None:
        self._a = a
        self._b = b

    def __str__(self) -> str:
        """Retorna a representação textual desta função."""
        return f"({self._a})+({self._b})"

    def __repr__(self) -> str:
        """Retorna a representação textual do contrutor desta função."""
        return f"{self.__class__.__qualname__}({self._a}, {self._b})"

    def __eq__(self, other):
        """Retorna verdadeiro se esta função é igual à constante `other`. Falso, caso contrário."""
        if super(Sum, self).__eq__(other):
            if self._b == other.u and self._a == other.radic:
                return True
        return False

    def __ne__(self, other):
        """Retorna verdadeiro se esta função é diferente de `other`. Falso, caso contrário."""
        if super(Sum, self).__eq__(other):
            if self._b != other.u or self._a != other.radic:
                return True
        return False

    @property
    def b(self) -> Union[Constant, FunctionABC]:
        """Lê o segundo termo desta função."""
        return self._b

    @property
    def a(self) -> Union[Constant, FunctionABC]:
        """Lê o primeiro termo desta função."""
        return self._a

    def copy(self) -> 'Product':
        """Retorna uma cópia deste produto."""
        return Product(self._a.copy(), self._b.copy())

    def derive(self) -> 'Sum':
        """Retorna a taxa de variação de `y = u * v`, que é `y' = u' + v'`."""
        return Sum(self._a.derive(), self._b.derive())

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor desta função. Os termos podem depender de `kwargs`."""
        return self._a.evaluate(**kwargs) + self._b.evaluate(**kwargs)


class Subtraction(FunctionABC):
    """Classe de função soma.

        Representa a subtração entre duas funções `u` e `v.
        Para `y = u - v` a derivada é `y' = u' - v'`.
        O valor desta função depende de ambos os termos.
        """

    __slots__ = '_a', '_b'

    def __init__(self, a: Union[Constant, Literal, FunctionABC], b: Union[Constant, Literal, FunctionABC]) -> None:
        self._a = a
        self._b = b

    def __str__(self) -> str:
        """Retorna a representação textual desta função."""
        return f"({self._a})-({self._b})"

    def __repr__(self) -> str:
        """Retorna a representação textual do contrutor desta função."""
        return f"{self.__class__.__qualname__}({self._a}, {self._b})"

    def __eq__(self, other):
        """Retorna verdadeiro se esta função é igual à constante `other`. Falso, caso contrário."""
        if super(Subtraction, self).__eq__(other):
            if self._b == other.index and self._a == other.radic:
                return True
        return False

    def __ne__(self, other):
        """Retorna verdadeiro se esta função é diferente de `other`. Falso, caso contrário."""
        if super(Subtraction, self).__eq__(other):
            if self._b != other.index or self._a != other.radic:
                return True
        return False

    @property
    def b(self) -> Union[Constant, FunctionABC]:
        """Lê o segundo termo desta função."""
        return self._b

    @property
    def a(self) -> Union[Constant, FunctionABC]:
        """Lê o primeiro termo desta função."""
        return self._a

    def copy(self) -> 'Subtraction':
        """Retorna uma cópia deste produto."""
        return self.__class__(self._a.copy(), self._b.copy())

    def derive(self) -> 'Subtraction':
        """Retorna a taxa de variação de `y = u - v`, que é `y' = u' - v'`."""
        return self.__class__(self._a.derive(), self._b.derive())

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor desta função. Os termos podem depender de `kwargs`."""
        return self._a.evaluate(**kwargs) - self._b.evaluate(**kwargs)


class Product(FunctionABC):
    """Classe de função multiplicação.

    Representa a multiplicação entre uma constante `k` e uma função `u` ou
    entre duas funções `u` e `v`.
    Para `y = k * u` a derivada é `y' = k * u'`;
    Para `y = u * v` a derivada é `y' = u' * v + u * v'`.
    O valor desta função depende de ambos os fatores.
    """

    __slots__ = '_a', '_b'

    def __init__(self, a: Union[Constant, FunctionABC], b: Union[Constant, FunctionABC]) -> None:
        self._a = a
        self._b = b

    def __str__(self) -> str:
        """Retorna a representação textual desta função."""
        a = str(self._a)
        if not isinstance(self._a, Constant):
            a = f"({self._a})"
        b = str(self._b)
        if not isinstance(self._b, Constant):
            b = f"({self._b})"
        return f"{a}*{b}"

    def __repr__(self) -> str:
        """Retorna a representação textual do contrutor desta função."""
        return f"{self.__class__.__qualname__}({self._a}, {self._b})"

    def __eq__(self, other):
        """Retorna verdadeiro se esta função é igual à constante `other`. Falso, caso contrário."""
        if super(Product, self).__eq__(other):
            if self._b == other.index and self._a == other.radic:
                return True
        return False

    def __ne__(self, other):
        """Retorna verdadeiro se esta função é diferente de `other`. Falso, caso contrário."""
        if super(Product, self).__eq__(other):
            if self._b != other.index or self._a != other.radic:
                return True
        return False

    @property
    def b(self) -> Union[Constant, FunctionABC]:
        """Lê o segundo fator desta função."""
        return self._b

    @property
    def a(self) -> Union[Constant, FunctionABC]:
        """Lê o primeiro fator desta função."""
        return self._a

    def copy(self) -> 'Product':
        """Retorna uma cópia deste produto."""
        return Product(self._a.copy(), self._b.copy())

    def derive(self) -> Union['Sum', 'Product']:
        """Retorna a taxa de variação de `y = u * v`, que é `y' = u' * v + u * v'` ou `y' = k * u'`."""
        a = self._a.__class__
        b = self._b.__class__
        if a != b and Constant in (a, b):
            if isinstance(self._a, Constant):
                return Product(self._a.copy(), self._b.derive())
            elif isinstance(self._b, Constant):
                return Product(self._b.copy(), self._a.derive())
        else:
            return Sum(Product(self._a.derive(), self._b.copy()), Product(self._a.copy(), self._b.derive()))

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor desta função. Os termos podem depender de `kwargs`."""
        return self._a.evaluate(**kwargs) * self._b.evaluate(**kwargs)


class Quotient(Product):
    """Classe de função divisão.

    Representa a divisão entre duas funções `u` e `v`.
    Para `y = u / v` a derivada é `y' = (u' * v - u * v') / v^2`.
    O valor desta função depende de ambos os termos.
    """

    def __str__(self) -> str:
        """Retorna a representação textual desta função."""
        d = str(self._b)
        if isinstance(self._b, Exponent):
            d = f"({self._b.u})^{self._b.v}"
        return f"[{self._a}]/{d}"

    def derive(self) -> Union['Quotient', 'Product']:
        """Retorna a taxa de variação de `y = u * v`, que é `(y' = u' * v - u * v') / v^2`."""
        return Quotient(
            Subtraction(
                Product(self._a.derive(), self._b.copy()),
                Product(self._a.copy(), self._b.derive())
            ),
            Exponent(self._b.copy(), Constant(2))
        )


class Radical(FunctionABC):
    """Classe de função raíz.

    Representa a raíz n-ésima de uma constante, literal ou função.
    A representação textual de um radical é `V(i_n)` onde `i` é o índice (opcional) e
    `n` é o radicando.
    Para `y = V(i_n^p)` a derivada é `y' = (p/i)*n^((p/i)-1)`.
    Para `y = V(i_u)`, onde `v = y` e `u` é uma função, a derivada é `y' * u'`.
    """

    def __init__(self, radic: Union[Constant, FunctionABC], index: Constant=DEFAULT) -> None:
        self._radic = radic
        self._index = Constant(2) if index is DEFAULT else index

    def __str__(self) -> str:
        """Retorna a representação textual desta funcão."""
        ind = '' if self._index.k == 2 else f"{self._index}_"
        if isinstance(self._radic, Exponent):
            return f"V({ind}{self._radic})"
        return f"V({ind}{self._radic})"

    def __repr__(self) -> str:
        """Retorna a representação textual desta funcão."""
        ind = '' if self._index.k == 2 else f", {self._index}"
        return f"{clsname(self)}({self._radic}{ind})"

    def __eq__(self, other):
        """Retorna verdadeiro se esta função é igual à constante `other`. Falso, caso contrário."""
        if super(Radical, self).__eq__(other):
            if self._index == other.index and self._radic == other.radic:
                return True
        return False

    def __ne__(self, other):
        """Retorna verdadeiro se esta função é diferente de `other`. Falso, caso contrário."""
        if super(Radical, self).__eq__(other):
            if self._index != other.index or self._radic != other.radic:
                return True
        return False

    @property
    def index(self) -> Constant:
        """Lê o segundo fator desta função."""
        return self._index

    @property
    def radic(self) -> Union[Constant, FunctionABC]:
        """Lê o primeiro fator desta função."""
        return self._radic

    def copy(self) -> 'Radical':
        """Retorna uma cópia deste produto."""
        return Radical(self._radic.copy(), self._index.copy())

    def derive(self) -> Union['Constant', 'Monomial', 'Product']:
        """Retorna a taxa de variação de `y = u * v`, que é `y' = u' * v + u * v'` ou `y' = k * u'`."""
        i = self._index
        r = self._radic

        if isinstance(r, Constant):
            return Constant(1)

        elif isinstance(r, Literal):
            e = Constant(1 / i.k)
            return Monomial(r.copy(), Constant(e.k - 1), e)

        elif isinstance(r, FunctionABC):
            if isinstance(r, Exponent):
                # retorna a derivada do radicando se o expoente for igual ao índice.
                if r.v == i:
                    return r.derive()

                # sendo r e i ambos constantes, a taxa de variação é 0.
                elif isinstance(r, Constant):
                    return Constant(0)

                ek: int = i.k
                d = Monomial(r.copy(), Constant(ek - 1), Constant(ek))
                return Product(d, r.derive())

    def evaluate(self, **kwargs) -> Union[int, float]:
        """Retorna o valor desta função. Os termos podem depender de `kwargs`."""
        i = self._index.k
        r = self._radic.evaluate(**kwargs)
        if r <= 0:
            print(f"Erro de domínio: radicando negativo em {self}; com {kwargs}")
            quit()
        elif i <= 0:
            print(f"Erro de domínio: índice negativo em {self}; com {kwargs}")
        return nroot(i, r)


if __name__ == '__main__':
    # f1 = Polinomial(Monomial(Literal('x'), Constant(3)), Monomial(Literal('x'), Constant(2), Constant(-5)))
    f2 = Radical(Exponent(Monomial(Literal('x'), Constant(2), Constant(3)), Constant(2)))
    df = f2.derive()
    print(repr(df))
    # print(f1, '->', df, ':', df.evaluate(x=2))
    print(f2, '->', df, ':', df.evaluate(x=2))
