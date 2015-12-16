#-*- encoding:utf-8 -*-
from __future__ import print_function
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

text = "这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。答谢宴于晚上8点开始。"
tr4w = TextRank4Keyword()

tr4w.analyze(text=text, lower=True, window=2)

print()
print('sentences:')
for s in tr4w.sentences:
    print(s)                 # py2中是unicode类型。py3中是str类型。

print()
print('words_no_filter')
for words in tr4w.words_no_filter:
    print('/'.join(words))   # py2中是unicode类型。py3中是str类型。

print()
print('words_no_stop_words')
for words in tr4w.words_no_stop_words:
    print('/'.join(words))   # py2中是unicode类型。py3中是str类型。

print()
print('words_all_filters')
for words in tr4w.words_all_filters:
    print('/'.join(words))   # py2中是unicode类型。py3中是str类型。