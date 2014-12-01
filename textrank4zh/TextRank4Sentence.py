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
        source: no_filter, no_stop_words, all_filters这三个值
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
        ''' '''
        words = list(set(word_list1 + word_list2))        
        vector1 = [float(word_list1.count(word)) for word in words]
        vector2 = [float(word_list2.count(word)) for word in words]
        return vector1, vector2
            
    def get_key_sentences(self, num = 6, sentence_min_len = 6):
        '''
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
    text = codecs.open('../text/03.txt', 'r', 'utf-8').read()
    # text = "坏人坏人坏人坏人坏人。你好"
    tr4s = TextRank4Sentence(stop_words_file='../stopword.data')
    tr4s.train(text=text, speech_tag_filter=True, lower=True, source = 'all_filters')
    
    print '\n'.join(tr4s.get_key_sentences(num=1))
