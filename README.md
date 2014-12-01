#TextRank4ZH
-----

TextRank算法可以用来从文本中提取关键词和摘要（重要的句子）。TextRank4ZH是针对中文文本的TextRank算法的python算法实现。


##安装

本程序使用python 2.7测试没有问题，暂时不兼容python 3。

先确定已经有jieba、numpy、networkx这三个库。可以使用`pip`安装：

```
$ sudo pip install numpy
$ sudo pip install jieba
$ sudo pip install networkx
```

关于库版本，以下作为参考：

```
$ pip show jieba
---
Name: jieba
Version: 0.35
Location: /usr/local/lib/python2.7/dist-packages
Requires: 
$ pip show numpy
---
Name: numpy
Version: 1.7.1
Location: /usr/lib/python2.7/dist-packages
Requires: 
$ pip show networkx
---
Name: networkx
Version: 1.9.1
Location: /usr/local/lib/python2.7/dist-packages
Requires: decorator

```

另外，请确保安装最新版本的jieba分词，TextRank4ZH需要新版本jieba提供的词性标注功能。

```
$ sudo pip install jieba --upgrade
```

TextRank4ZH暂不支持使用easy_install、pip来安装，使用者可以将`textrank4zh`拷贝到项目目录，或者环境变量`PYTHONPATH`指向的目录中。

##目录结构

```
├── LICENSE         #许可证
├── README.md       #使用说明
├── stopword.data   #停止词词典
├── test.py         #测试
├── text            #存放测试所需要的文本
│   ├── 01.txt
│   ├── 02.txt
│   ├── 03.txt
│   ├── 04.txt
│   └── 05.txt
└── textrank4zh     #!main
    ├── __init__.py
    ├── Segmentation.py
    ├── TextRank4Keyword.py
    └── TextRank4Sentence.py
```

##原理

TextRank的详细原理请参考：

> Mihalcea R, Tarau P. TextRank: Bringing order into texts[C]. Association for Computational Linguistics, 2004.

###关键词提取
将原文本拆分为句子，在每个句子中过滤掉停用词（可选），并只保留指定词性的单词（可选）。由此可以得到句子的集合和单词的集合。

每个单词作为pagerank中的一个节点。设定窗口大小为k，假设一个句子依次由下面的单词组成：
```
w1, w2, w3, w4, w5, ..., wn
```
`w1, w2, ..., wk`、`w2, w3, ...,wk+1`、`w3, w4, ...,wk+2`等都是一个窗口。在一个窗口中的任两个单词对应的节点之间存在一个无向无权的边。

基于上面构成图，可以计算出每个单词节点的重要性。最重要的若干单词可以作为关键词。


###关键短语提取
参照[关键词提取](#关键词提取)提取出若干关键词。若原文本中存在若干个关键词相邻的情况，那么这些关键词可以构成一个关键词组。

例如，在一篇介绍`支持向量机`的文章中，可以找到关键词`支持`、`向量`、`机`，通过关键词组提取，可以得到`支持向量机`。

###摘要生成
将每个句子看成图中的一个节点，若两个句子之间有相似性，认为对应的两个节点之间有一个无向有权边，权值是相似度。

通过pagerank算法计算得到的重要性最高的若干句子可以当作摘要。





##测试

`test.py`提供了使用的示例：
```
#-*- encoding:utf-8 -*-

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

text = codecs.open('./text/01.txt', 'r', 'utf-8').read()
tr4w = TextRank4Keyword(stop_words_file='./stopword.data')  # 导入停止词

#使用词性过滤，文本小写，窗口为2
tr4w.train(text=text, speech_tag_filter=True, lower=True, window=2)  

print '关键词：'
# 20个关键词且每个的长度最小为1
print '/'.join(tr4w.get_keywords(20, word_min_len=1))  

print '关键短语：'
# 20个关键词去构造短语，短语在原文本中出现次数最少为2
print '/'.join(tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2))  
    
tr4s = TextRank4Sentence(stop_words_file='./stopword.data')

# 使用词性过滤，文本小写，使用words_all_filters生成句子之间的相似性
tr4s.train(text=text, speech_tag_filter=True, lower=True, source = 'all_filters')

print '摘要：'
print '\n'.join(tr4s.get_key_sentences(num=3)) # 重要性最高的三个句子
```

得到的关键词：
```
媒体/高圆圆/微/宾客/赵又廷/答谢/谢娜/现身/记者/新人/北京/博/展示/捧场/礼物/张杰/当晚/戴/酒店/外套
```
得到的关键短语：
```
微博
```

得到的摘要：
```
中新网北京12月1日电(记者 张曦) 30日晚，高圆圆和赵又廷在京举行答谢宴，诸多明星现身捧场，其中包括张杰(微博)、谢娜(微博)夫妇、何炅(微博)、蔡康永(微博)、徐克、张凯丽、黄轩(微博)等
高圆圆身穿粉色外套，看到大批记者在场露出娇羞神色，赵又廷则戴着鸭舌帽，十分淡定，两人快步走进电梯，未接受媒体采访
记者了解到，出席高圆圆、赵又廷答谢宴的宾客近百人，其中不少都是女方的高中同学
```

##使用说明

类TextRank4Keyword、TextRank4Sentence在处理一段文本时会将文本拆分成4种格式：

**sentences：**由句子组成的列表。

**words_no_filter：**对sentences中每个句子分词而得到的两级列表。

**words_no_stop_words：**去掉words_no_filter中的停止词而得到的两级列表。

**words_all_filters：**保留words_no_stop_words中指定词性的单词而得到的两级列表。

例如，对于：
```
这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。答谢宴于晚上8点开始。
```
对类TextRank4Sentence，在`speech_tag_filter=True, lower=True, source = 'all_filters'`时，

sentences：
```
['这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足', 
'答谢宴于晚上8点开始']
```

words_no_filter：
```
[
    [ '这', '间, '酒店, '位于, '北京, '东三环, '里面, '摆放, '很多, '雕塑, '文艺, '气息, '十足'],
    [ '答谢', '宴于, '晚上, '8, '点, '开始' ]
]
```

words_no_stop_words：
```
[
    [ '间', '酒店, '位于, '北京, '东三环, '里面, '摆放, '很多, '雕塑, '文艺, '气息, '十足' ],
    [ '答谢', '宴于, '晚上, '8, '点' ]
]
```
words_all_filters：

```
[
    [ '酒店', '位于, '北京, '东三环, '摆放, '雕塑, '文艺, '气息' ],
    [ '答谢', '宴于, '晚上' ]
]
```

类TextRank4Keyword位于`textrank4zh/TextRank4Keyword.py`中，类TextRank4Sentence位于`textrank4zh/TextRank4Sentence.py`中，**类的实现、函数的参数请参考源码注释。**










