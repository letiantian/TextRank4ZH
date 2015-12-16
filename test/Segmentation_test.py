#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import Segmentation

seg = Segmentation.Segmentation()

text = codecs.open('./doc/01.txt', 'r', 'utf-8', 'ignore').read()
text = "视频里，我们的杰宝热情地用英文和全场观众打招呼并清唱了一段《Heal The World》。我们的世界充满了未知数。"

result = seg.segment(text=text, lower=True)

for key in result:
    print(key)

print(20*'#')
for s in result['sentences']:
    print(s)

print(20*'*')
for s in result.sentences:
    print (s)

print
for ss in result.words_no_filter:
    print( '  '.join(ss) )

print
for ss in result.words_no_stop_words:
    print( ' / '.join(ss) )

print
for ss in result.words_all_filters:
    print (' | '.join(ss) )
