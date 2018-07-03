# TextRank4ZH

TextRank算法可以用来从文本中提取关键词和摘要（重要的句子）。TextRank4ZH是针对中文文本的TextRank算法的python算法实现。

## 安装

方式1：
```
$ python setup.py install --user
```

方式2：
```
$ sudo python setup.py install
```

方式3：
```
$ pip install textrank4zh --user
```

方式4：
```
$ sudo pip install textrank4zh
```

Python 3下需要将上面的python改成python3，pip改成pip3。


## 卸载
```plain
$ pip uninstall textrank4zh
```

## 依赖
jieba >= 0.35  
numpy >= 1.7.1  
networkx >= 1.9.1  

## 兼容性
在Python 2.7.9和Python 3.4.3中测试通过。


## 原理

TextRank的详细原理请参考：

> Mihalcea R, Tarau P. TextRank: Bringing order into texts[C]. Association for Computational Linguistics, 2004.

关于TextRank4ZH的原理和使用介绍：[使用TextRank算法为文本生成关键字和摘要](https://www.letiantian.me/2014-12-01-text-rank/)

### 关键词提取
将原文本拆分为句子，在每个句子中过滤掉停用词（可选），并只保留指定词性的单词（可选）。由此可以得到句子的集合和单词的集合。

每个单词作为pagerank中的一个节点。设定窗口大小为k，假设一个句子依次由下面的单词组成：
```
w1, w2, w3, w4, w5, ..., wn
```
`w1, w2, ..., wk`、`w2, w3, ...,wk+1`、`w3, w4, ...,wk+2`等都是一个窗口。在一个窗口中的任两个单词对应的节点之间存在一个无向无权的边。

基于上面构成图，可以计算出每个单词节点的重要性。最重要的若干单词可以作为关键词。


### 关键短语提取
参照[关键词提取](#关键词提取)提取出若干关键词。若原文本中存在若干个关键词相邻的情况，那么这些关键词可以构成一个关键词组。

例如，在一篇介绍`支持向量机`的文章中，可以找到关键词`支持`、`向量`、`机`，通过关键词组提取，可以得到`支持向量机`。

### 摘要生成
将每个句子看成图中的一个节点，若两个句子之间有相似性，认为对应的两个节点之间有一个无向有权边，权值是相似度。

通过pagerank算法计算得到的重要性最高的若干句子可以当作摘要。


## 示例
见[example](./example)、[test](./test)。

example/example01.py:

```python
#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

text = codecs.open('../test/doc/01.txt', 'r', 'utf-8').read()
tr4w = TextRank4Keyword()

tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

print( '关键词：' )
for item in tr4w.get_keywords(20, word_min_len=1):
    print(item.word, item.weight)

print()
print( '关键短语：' )
for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
    print(phrase)

tr4s = TextRank4Sentence()
tr4s.analyze(text=text, lower=True, source = 'all_filters')

print()
print( '摘要：' )
for item in tr4s.get_key_sentences(num=3):
    print(item.index, item.weight, item.sentence)  # index是语句在文本中位置，weight是权重
```

运行结果如下：
```plain
关键词：
媒体 0.02155864734852778
高圆圆 0.020220281898126486
微 0.01671909730824073
宾客 0.014328439104001788
赵又廷 0.014035488254875914
答谢 0.013759845912857732
谢娜 0.013361244496632448
现身 0.012724133346018603
记者 0.01227742092899235
新人 0.01183128428494362
北京 0.011686712993089671
博 0.011447168887452668
展示 0.010889176260920504
捧场 0.010507502237123278
礼物 0.010447275379792245
张杰 0.009558332870902892
当晚 0.009137982757893915
戴 0.008915271161035208
酒店 0.00883521621207796
外套 0.008822082954131174

关键短语：
微博

摘要：
摘要：
0 0.0709719557171 中新网北京12月1日电(记者 张曦) 30日晚，高圆圆和赵又廷在京举行答谢宴，诸多明星现身捧场，其中包括张杰(微博)、谢娜(微博)夫妇、何炅(微博)、蔡康永(微博)、徐克、张凯丽、黄轩(微博)等
6 0.0541037236415 高圆圆身穿粉色外套，看到大批记者在场露出娇羞神色，赵又廷则戴着鸭舌帽，十分淡定，两人快步走进电梯，未接受媒体采访
27 0.0490428312984 记者了解到，出席高圆圆、赵又廷答谢宴的宾客近百人，其中不少都是女方的高中同学

```

## 使用说明

类TextRank4Keyword、TextRank4Sentence在处理一段文本时会将文本拆分成4种格式：

* sentences：由句子组成的列表。
* words_no_filter：对sentences中每个句子分词而得到的两级列表。
* words_no_stop_words：去掉words_no_filter中的停止词而得到的二维列表。
* words_all_filters：保留words_no_stop_words中指定词性的单词而得到的二维列表。

例如，对于：
```
这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足。答谢宴于晚上8点开始。
```

```python
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
```

运行结果如下：
```plain
sentences:
这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足
答谢宴于晚上8点开始

words_no_filter
这/间/酒店/位于/北京/东三环/里面/摆放/很多/雕塑/文艺/气息/十足
答谢/宴于/晚上/8/点/开始

words_no_stop_words
间/酒店/位于/北京/东三环/里面/摆放/很多/雕塑/文艺/气息/十足
答谢/宴于/晚上/8/点

words_all_filters
酒店/位于/北京/东三环/摆放/雕塑/文艺/气息
答谢/宴于/晚上

```


## API
TODO.

类的实现、函数的参数请参考源码注释。

## License
[MIT](./LICENSE)









