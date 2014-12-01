#-*- encoding:utf-8 -*-
'''
Created on Nov 30, 2014
@author: letian
'''

import networkx as nx
from Segmentation import Segmentation
import numpy as np

class TextRank4Keyword(object):
    
    def __init__(self, stop_words_file = None, delimiters = '?!;？！。；…\n'):
        ''' '''
        self.text = ''
        self.keywords = []
        
        self.seg = Segmentation(stop_words_file=stop_words_file, delimiters=delimiters)
        
        self.words_no_filter = None     # 2维列表
        self.words_no_stop_words = None
        self.words_all_filters = None
        
        self.word_index = {}
        self.index_word = {}
        self.graph = None
        
    def train(self, text, window = 2, lower = False, speech_tag_filter=True, 
              vertex_source = 'all_filters',
              edge_source = 'no_stop_words'):
        '''
        vertex_source, edge_source: no_filter, no_stop_words, all_filters这三个值
        '''
        
        self.text = text
        self.word_index = {}
        self.index_word = {}
        self.keywords = []
        self.graph = None
        
        (_, self.words_no_filter, self.words_no_stop_words, self.words_all_filters) = self.seg.segment(text=text, 
                                                                                                     lower=lower, 
                                                                                                     speech_tag_filter=speech_tag_filter)
        
        if vertex_source == 'no_filter':
            vertex_source = self.words_no_filter
        elif vertex_source == 'no_stop_words':
            vertex_source = self.words_no_stop_words
        else:
            vertex_source = self.words_all_filters

        if edge_source == 'no_filter':
            edge_source = self.words_no_filter
        elif vertex_source == 'all_filters':
            edge_source = self.words_all_filters
        else:
            edge_source = self.words_no_stop_words
            
        
        
        index = 0
        for words in vertex_source:
            for word in words:
                if not self.word_index.has_key(word):
                    self.word_index[word] = index
                    self.index_word[index] = word
                    index += 1
        
        words_number = index # 单词数量
        self.graph = np.zeros((words_number, words_number))
        
        for word_list in edge_source:
            for w1, w2 in self.combine(word_list, window):
                if not self.word_index.has_key(w1):
                    continue
                if not self.word_index.has_key(w2):
                    continue
                index1 = self.word_index[w1]
                index2 = self.word_index[w2]
                self.graph[index1][index2] = 1.0
                self.graph[index2][index1] = 1.0
        
        for x in xrange(words_number):
            row_sum = np.sum(self.graph[x, :])
            if row_sum > 0:
                self.graph[x, :] = self.graph[x, :] / row_sum
        
        nx_graph = nx.from_numpy_matrix(self.graph)
        scores = nx.pagerank(nx_graph) # this is a dict
        sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse=True)
        for index, _ in sorted_scores:
            self.keywords.append(self.index_word[index])
            
        
 
    
    def combine(self, word_list, window = 2):
        ''' '''
        window = int(window)
        if window < 2: window = 2
        for x in xrange(1, window):
            if x >= len(word_list):
                break
            word_list2 = word_list[x:]
            res = zip(word_list, word_list2)
            for r in res:
                yield r
    
    def get_keywords(self, num = 6, word_min_len = 1):
        '''
        '''
        result = []
        count = 0
        for word in self.keywords:
            if count >= num:
                break
            if len(word) >= word_min_len:
                result.append(word)
                count += 1
        return result
    
    def get_keyphrases(self, keywords_num = 12, min_occur_num = 2): 
        ''' 获取关键词组 '''
        keywords_set = set(self.get_keywords(num=keywords_num, word_min_len = 1))
            
        keyphrases = set()
        one = []
        for sentence_list in self.words_no_filter:
            for word in sentence_list:
                # print '/'.join(one)
                # print word
                if word in keywords_set:
                    one.append(word)
                else:
                    if len(one)>1:
                        keyphrases.add(''.join(one))
                        one = []
                        continue
                    one = []
                    
        return [phrase for phrase in keyphrases 
                if self.text.count(phrase) >= min_occur_num]


if __name__ == '__main__':
    import codecs
    text = codecs.open('../text/02.txt', 'r', 'utf-8').read()
    
    # text = "坏人"
    tr4w = TextRank4Keyword(stop_words_file='../stopword.data')
    tr4w.train(text=text, speech_tag_filter=True, lower=True, window=2)
    
    for word in tr4w.get_keywords(10, word_min_len=2):
        print word
    
    print '---'
    
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
        print phrase
        

        