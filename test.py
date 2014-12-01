#-*- encoding:utf-8 -*-
'''
Created on Dec 1, 2014
@author: letian
'''

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

text = codecs.open('./text/01.txt', 'r', 'utf-8').read()
tr4w = TextRank4Keyword(stop_words_file='./stopword.data')
tr4w.train(text=text, speech_tag_filter=True, lower=True, window=2)

print
print '/'.join(tr4w.get_keywords(10, word_min_len=2))

print
print '/'.join(tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2))
    
tr4s = TextRank4Sentence(stop_words_file='./stopword.data')
tr4s.train(text=text, speech_tag_filter=True, lower=True, source = 'all_filters')

print
print '\n'.join(tr4s.get_key_sentences(num=3))