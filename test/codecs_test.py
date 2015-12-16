#-*- encoding:utf-8 -*-
from __future__ import print_function


import codecs
text = codecs.open('./doc/01.txt', 'r', 'utf-8', 'ignore').read()
print( type(text) )  # in py2 is unicode, py3 is str