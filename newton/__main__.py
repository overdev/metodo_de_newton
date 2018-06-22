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

import sys
import os
import newton as newton
import pnlexer as pnlexer
from typing import List, Union, Tuple
from enum import Enum


USAGE = """Exemplos de utilização:
Entrada direta dos argumentos:
    >>> python newton "3x^4-x^3+7x^2-8" x=-2 kmax=100000 e=0.000001
    onde:
        x    -> valor inicial de x
        kmax -> máximo de iterações
        e    -> epsilon
    ou
    >>> python newton "3x^4-x^3+7x^2-8" -2 100000 0.000001

Processamento em lote:
    >>> python newton ./entrada.txt
    ou
    >>> python newton ./entrada.txt ./saida.txt

Argumentos opcionais:
    verbose -> Imprime a saída do resultado de maneira mais legível.
"""


class IOKind(Enum):
    STD = 0
    FILE = 1


class Context:
    """Classe de contexto Context.

    Representa o contexto de execução deste programa.
    """

    def __init__(self, *argv) -> None:
        self.argv: List[str] = argv
        self.input_kind: IOKind = IOKind.STD
        self.output_kind: IOKind = IOKind.STD
        self.input_file = None
        self.output_file = None
        self.input_data: List[str] = []
        self.output_data: List[str] = []
        self.verbose: bool = True
        self.function_string: str = ''
        self.function_args: List[Union[bool, int, float]] = []
        self.default_x: int = 1
        self.default_kmax: int = 100000
        self.default_e: int = 0.0001
        self.default_verbose: bool = False

    def run(self):
        argv = self.argv
        argc: int = len(argv)
        e: float = self.default_e
        initial_x: Union[int, float] = self.default_x
        kmax: int = self.default_kmax

        print("ARGUMENTS:", argv)
        if argc == 1:
            print(USAGE)

        if argc == 2 or argc == 3:
            # arg2 deve ser o caminho para um arquivo
            if os.path.isfile(argv[1]):
                if not os.path.exists(argv[1]):
                    print(f"Erro de entrada: '{argv[1]}' não é um caminho válido de arquivo, ou o arquivo não existe.")
                    quit()

                if argc == 3:
                    if argv[2].lower() == 'verbose':
                        self.verbose = True
                    else:
                        if not os.path.isfile(argv[2]):
                            print(f"Saída: '{argv[2]}' não é um caminho válido de arquivo.")
                            quit()
                        self.output_kind = IOKind.FILE
                        self.output_file = argv[2]

                self.input_kind = IOKind.FILE
                self.input_file = argv[1]

            print("-----", self.input_kind, self.output_kind)

        if argv == 4:
            print("Número insuficiente de argumentos (4).")

        if argc >= 5:
            print(argv[1])
            func: str = argv[1].strip('\'\"')
            if not func.endswith(';'):
                func = f"{func};"

            if 'verbose' in argv[5:]:
                self.verbose = True

            e, initial_x, kmax = self.get_argument_values(argv[2], argv[3], argv[4])
            print("K_MAX", kmax, argv[3])

            self.function_string = func

        print("\nProcessando. Por favor, espere...\n")
        if self.input_kind is IOKind.STD:
            scanner: pnlexer.Scanner = pnlexer.Scanner(self.function_string)
            fn: pnlexer.F = scanner.scan()

            output: str = newton.newton_raphson(fn, e, initial_x, kmax, self.verbose)

            self.output_data.append(output)

        else:
            self.process_input_data()

        self.save_output()

    def get_argument_values(self, arg1: str, arg2: str, arg3: str) -> Tuple[float, int, Union[int, float]]:
        arguments: List[str] = []
        e: float = self.default_e
        initial_x: Union[int, float] = self.default_x
        kmax: int = self.default_kmax

        for argname, arg in (('e', arg1), ('x', arg2), ('k', arg3)):
            name, value = self.parse_argument(arg)
            if name.lower() in ('e', 'eps', 'epsilon', 'erro'):
                e = value
            elif name.lower() in ('x', 'x0', 'x_0', 'inicial', 'xinicial', 'x_inicial'):
                initial_x = value
            elif name.lower() in ('k', 'kmax', 'k_max', 'i', 'imax', 'i_max', 'max', 'iter'):
                kmax = value
            else:
                if argname == 'e':
                    e = value
                elif argname == 'x':
                    initial_x = value
                elif argname == 'k':
                    kmax = value

            arguments.append(argname)

        return e, initial_x, kmax

    def parse_argument(self, arg: str) -> Tuple[str, Union[int, float]]:
        value = 0
        name = ''
        split: str = arg.split('=')
        if split[0] == arg:
            try:
               value = eval(split[0])
               assert isinstance(value, (int, float))
            except (SyntaxError, AssertionError):
                print(f"Argumento inválido: '{arg}'")
                quit()
        elif len(split) == 2:
            try:
               value = eval(split[1])
               name = split[0]
               assert isinstance(value, (int, float))
            except (SyntaxError, AssertionError):
                print(f"Argumento inválido: '{arg}'")
                quit()

        return name, value

    def process_input_data(self) -> None:
        self.load_input()
        if self.input_kind is IOKind.FILE:
            for line in self.input_data:
                self.parse_input_line(line)

    def parse_input_line(self, line: str) -> None:
        if line.lower().startswith('default'):
            print(f"Alterando argumentos padrão: {line}")
            self.set_defaults(line)
        else:
            print(f"Processando {line}")
            self.process_input_line(line)

    def set_defaults(self, line: str) -> None:
        parts: List[str] = line.strip().split()
        n = len(parts)

        if n == 0:
            return

        if n == 1:
            return

        if n >= 2:
            if parts[1].lower() != 'verbose':
                self.default_x = self.parse_argument(parts[1].strip())
            else:
                self.default_verbose = True

        if n >= 3:
            if parts[2].lower() != 'verbose':
                self.default_kmax: int = self.parse_argument(parts[2].strip())
            else:
                self.default_verbose = True

        if n >= 4:
            if parts[3].lower() != 'verbose':
                self.default_e: float = self.parse_argument(parts[3].strip())
            else:
                self.default_verbose = True

    def process_input_line(self, line: str) -> None:
        parts: List[str] = line.strip().split()
        n = len(parts)
        func_str: str = ''
        verbose: bool = self.default_verbose
        arg1 = f'e={self.default_e}'
        arg2 = f'x={self.default_x}'
        arg3 = f'k={self.default_kmax}'

        if n == 0:
            return

        if n >= 1:
            func_str: str = parts[0].strip().strip('\'\"')

        if n >= 2:
            if parts[1].lower() != 'verbose':
                arg1 = parts[1].strip()
            else:
                verbose = True

        if n >= 3:
            if parts[2].lower() != 'verbose':
                arg2 = parts[2].strip()
            else:
                verbose = True

        if n >= 4:
            if parts[3].lower() != 'verbose':
                arg3 = parts[3].strip()
            else:
                verbose = True

        if n >= 5:
            if parts[4].lower() == 'verbose':
                verbose = True

        e, initial_x, kmax = self.get_argument_values(arg1, arg2, arg3)

        scanner: pnlexer.Scanner = pnlexer.Scanner(func_str)
        func: pnlexer.F = scanner.scan()
        output: str = newton.newton_raphson(func, e, initial_x, kmax, verbose)
        self.output_data.append(output)

    def load_input(self) -> None:
        if self.input_kind is IOKind.FILE:
            with open(self.input_file, 'r', encoding='utf8') as batch_input:
                self.input_data = batch_input.readlines()

    def save_output(self) -> None:
        if self.output_kind is IOKind.FILE:
            with open(self.output_file, 'w', encoding='utf8') as batch_output:
                for line in self.output_data:
                    print(line, file=batch_output)
        else:
            for line in self.output_data:
                print(line)


c = Context(*sys.argv)
c.run()