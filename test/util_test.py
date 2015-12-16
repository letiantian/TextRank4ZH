#-*- encoding:utf-8 -*-
from __future__ import print_function

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

def testDebug():
    import sys
    print(sys.getdefaultencoding())
    util.debug('你好')
    util.debug(u'世界')


if __name__ == "__main__":
    testAttrDict()
    testCombine()
    testDebug()
