#-*- encoding:utf-8 -*-
'''
Created on Dec 1, 2014
@author: letian
'''
import networkx as nx
from Segmentation import Segmentation
import numpy as np
import math

class TextRank4Sentence(object):
    
    def __init__(self, stop_words_file = None, delimiters='?!;？！。；…\n'):
        '''
        `stop_words_file`：默认值为None，此时内部停止词表为空；可以设置为文件路径（字符串），将从停止词文件中提取停止词。
        `delimiters`：默认值是`'?!;？！。；…\n'`，用来将文本拆分为句子。
        
        self.sentences：由句子组成的列表。
        self.words_no_filter：对sentences中每个句子分词而得到的两级列表。
        self.words_no_stop_words：去掉words_no_filter中的停止词而得到的两级列表。
        self.words_all_filters：保留words_no_stop_words中指定词性的单词而得到的两级列表。
        '''
        self.seg = Segmentation(stop_words_file=stop_words_file, delimiters=delimiters)
        
        self.sentences = None
        self.words_no_filter = None     # 2维列表
        self.words_no_stop_words = None
        self.words_all_filters = None
        
        self.graph = None
        self.key_sentences = None
        
    def train(self, text, lower = False, speech_tag_filter=True,
              source = 'no_stop_words', sim_func = 'standard'):
        ''' 
       `text`：文本内容，字符串。
        `lower`：是否将文本转换为小写。默认为False。
        `speech_tag_filter`：若值为True，将调用内部的词性列表来过滤生成words_all_filters。
                        若值为False，words_all_filters与words_no_stop_words相同。
        `source`：选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来生成句子之间的相似度。
                默认值为`'all_filters'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'`。
        `sim_func`： 指定计算句子相似度的函数。当前只有一个函数，对应默认值`standard`。
        '''
        
        self.key_sentences = []
        
        (self.sentences, self.words_no_filter, self.words_no_stop_words, self.words_all_filters) = self.seg.segment(text=text,  
                                                                                                                    lower=lower, 
                                                                                                                    speech_tag_filter=speech_tag_filter);
        # -
        
        # print self.sentences   
                                                                                                          
        if source == 'no_filter':
            source = self.words_no_filter
        elif source == 'all_filters':
            source = self.words_all_filters
        else:
            source = self.words_no_stop_words
            
        sim_func = self._get_similarity_standard
        
        sentences_num = len(source)
        
        self.graph = np.zeros((sentences_num, sentences_num))
        
        for x in xrange(sentences_num):
            for y in xrange(x, sentences_num):
                similarity = sim_func(source[x], source[y])
                self.graph[x, y] = similarity
                self.graph[y, x] = similarity
                
        for x in xrange(sentences_num):
            row_sum = np.sum(self.graph[x, :])
            if row_sum > 0:
                self.graph[x, :] = self.graph[x, :] / row_sum
                
        # print self.graph
                
        nx_graph = nx.from_numpy_matrix(self.graph)
        scores = nx.pagerank(nx_graph) # this is a dict
        sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse=True)
        
        # print sorted_scores
        
        for index, _ in sorted_scores:
            self.key_sentences.append(self.sentences[index])
            
        # print '\n'.join(self.key_sentences)
        

    def _get_similarity_standard(self, word_list1, word_list2):
        ''' 
        默认的用于计算两个句子相似度的函数。
        word_list1, word_list2: 分别代表两个句子，都是由单词组成的列表
        '''
        vector1, vector2 =self._gen_vectors(word_list1, word_list2)
        
        # print vector1, vector2
        
        vector3 = [vector1[x]*vector2[x]  for x in xrange(len(vector1))]
        vector4 = [1 for num in vector3 if num > 0.]
        co_occur_num = sum(vector4)
        
        # print co_occur_num
        
        if co_occur_num == 0.:
            return 0.
        
        denominator = math.log(float(len(word_list1))) + math.log(float(len(word_list2))) # 分母
        
        if denominator == 0.:
            return 0.
        
        return co_occur_num / denominator
        
        
    def _gen_vectors(self, word_list1, word_list2):
        '''
        两个句子转换成两个同样大小向量。可以通过这两个向量来计算两个句子的相似度。
        word_list1, word_list2: 分别代表两个句子，都是由单词组成的列表
        '''
        words = list(set(word_list1 + word_list2))        
        vector1 = [float(word_list1.count(word)) for word in words]
        vector2 = [float(word_list2.count(word)) for word in words]
        return vector1, vector2
            
    def get_key_sentences(self, num = 6, sentence_min_len = 6):
        '''
        获取最重要的num个长度大于等于sentence_min_len的句子用来生成摘要。
        返回列表。
        '''
        result = []
        count = 0
        for sentence in self.key_sentences:
            if count >= num:
                break
            if len(sentence) >= sentence_min_len:
                result.append(sentence)
                count += 1
        return result
    
if __name__ == '__main__':

    import codecs
    # text = codecs.open('../text/03.txt', 'r', 'utf-8').read()
    text = "这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。答谢宴于晚上8点开始。"
    tr4s = TextRank4Sentence(stop_words_file='../stopword.data')
    tr4s.train(text=text, speech_tag_filter=True, lower=True, source = 'all_filters')
    print '\n'.join(tr4s.get_key_sentences(num=1))
    
    print '\n'.join(tr4s.sentences)
    for wl in tr4s.words_no_filter:
        print '[', ', \''.join(wl), ']'
    print
    for wl in tr4s.words_no_stop_words:
        print '[', ', \''.join(wl), ']'
    print
    for wl in tr4s.words_all_filters:
        print '[', ', \''.join(wl), ']'