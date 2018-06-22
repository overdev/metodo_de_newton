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

import datetime
from typing import Union
from pnlexer import F


__all__ = [
    'newton_raphson'
]


OUTPUT_VERBOSE = """\n\n{func} -> {df} para X inicial {initial_x}, e {max_iterations} iterações.
-------------------------------------------------------------------------------
               Total de iterações: {iteration}
             x na última iteração: {x}
                      Epsilon (E): {epsilon}
          f(x) na última iteração: {eps}
     Tempo de execução (h:m:s:µs): {delta}

"""

OUTPUT = "y={func} y'={df} e={epsilon} x={x} k={iteration}/{max_iterations} f(x)={eps}  tempo={delta}"


def newton_raphson(func: F, epsilon: float, initial_x: Union[int, float], max_iterations: int,
                   verbose: bool=False) -> str:
    iteration: int = 0
    eps: int = 100000
    x: Union[int, float] = initial_x
    df = func.derive()

    now = datetime.datetime.now()
    while abs(eps) > epsilon and iteration < max_iterations:
        eps = func.eval(x=x) / df.eval(x=x)
        x -= eps
        iteration += 1
    delta = datetime.datetime.now() - now

    if verbose:
        return OUTPUT_VERBOSE.format(
            func=func,
            df=df,
            initial_x=initial_x,
            max_iterations=max_iterations,
            iteration=iteration,
            x=x,
            epsilon=epsilon,
            eps=eps,
            delta=delta
        )
    else:
        return OUTPUT.format(
            func=func,
            df=df,
            initial_x=initial_x,
            max_iterations=max_iterations,
            iteration=iteration,
            x=x,
            epsilon=epsilon,
            eps=eps,
            delta=delta
        )
