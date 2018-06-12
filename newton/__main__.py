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

import unicodedata
import sys
import classes


sup1 = unicodedata.lookup("Superscript One")
sup7 = unicodedata.lookup("Superscript Seven")
sup9 = unicodedata.lookup("Superscript Nine")
sqr = unicodedata.lookup("Square Root")
div = unicodedata.lookup("Subtraction Sign")

def print_help() -> None:
    s = """Modo de uso:
    
    A elaborar...
    """
    print(s)

def declare(out=None) -> None:
    global func, initial_val, iterations, epsilon
    print(f"7{div}3x{sup7} Executar função {func} com valor inicial {initial_val}, em até {iterations} iterações e com precisão {epsilon}", file=out)


args = sys.argv.copy()
argc = len(args)
immediate = False
extern_output = False

func = ''
initial_val = ''
iterations = ''
epsilon = ''
source = ''
dest = ''

if argc == 5:
    _, func, initial_val, iterations, epsilon = args
    immediate = True

elif argc == 3:
    _, source, dest = args
    extern_output = True

elif argc == 2:
    _, source = args

else:
    print_help()

if immediate:
    declare()

else:
    with open(source) as src:
        dst = open(dest, 'w', encoding='utf8') if extern_output else None
        for line in src:
            func, initial_val, iterations, epsilon = line.split(',')
            declare(dst)

        if extern_output:
            dst.close()