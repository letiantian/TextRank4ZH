#-*- encoding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys

from textrank4zh import util

def testAttrDict():
    r = util.AttrDict(a=2)
    print( r )
    print( r.a )
    print( r['a'] )

def testCombine():
    print(20*'*')
    for item in util.combine(['a', 'b', 'c', 'd'], 2):
        print(item)
    print
    for item in util.combine(['a', 'b', 'c', 'd'], 3):
        print (item)
     
if __name__ == "__main__":
    testAttrDict()
    testCombine()
