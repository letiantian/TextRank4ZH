#TextRank4ZH
-----

TextRank算法可以用来从文本中提取关键词和摘要（重要的句子）。TextRank4ZH是针对中文文本的TextRank算法的python算法实现。


##安装

本程序使用python2.7测试没有问题。

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

Text的详细原理请参考：

> Mihalcea R, Tarau P. TextRank: Bringing order into texts[C]. Association for Computational Linguistics, 2004.

###关键词提取
将原文本拆分为句子，在每个句子中过滤掉停用词（可选），并只保留指定词性的单词（可选）。由此可以得到句子的集合和单词的集合。

每个单词作为pagerank中的一个节点。设定窗口大小为k，假设一个句子依次由下面的单词组成：
```
w1, w2, w3, w4, w5, ..., wn
```
`w1, w2, ..., wk`、`w2, w3, ...,wk+1`、`w3, w4, ...,wk+2`等都是一个窗口。在一个窗口中的任两个单词对应的节点之间存在一个无向无权的边。

基于上面构成图，可以计算出每个单词节点的重要性。最重要的若干单词可以作为关键词。


###关键词组提取
参照[关键词提取](#关键词提取)提取出若干关键词。若原文本中存在若干个关键词相邻的情况，那么这些关键词可以构成一个关键词组。

例如，在一篇介绍`支持向量机`的文章中，可以找到关键词`支持`、`向量`、`机`，通过关键词组提取，可以得到`支持向量机`。

###摘要生成
将每个句子看成图中的一个节点，若两个句子之间有相似性，认为对应的两个节点之间有一个无向有权边，权值是相似性。

通过pagerank算法计算得到的重要性最高的若干句子可以当作摘要。





##测试

`test.py`提供了使用的示例。

得到的关键词：
```
媒体/高圆圆/宾客/新人/记者/北京/赵又廷/谢娜/现身/答谢
```
没有关键词组。

得到的摘要：
```
中新网北京12月1日电(记者 张曦) 30日晚，高圆圆和赵又廷在京举行答谢宴，诸多明星现身捧场，其中包括张杰(微博)、谢娜(微博)夫妇、何炅(微博)、蔡康永(微博)、徐克、张凯丽、黄轩(微博)等
高圆圆身穿粉色外套，看到大批记者在场露出娇羞神色，赵又廷则戴着鸭舌帽，十分淡定，两人快步走进电梯，未接受媒体采访
30日中午，有媒体曝光高圆圆和赵又廷现身台北桃园机场的照片，照片中两人小动作不断，尽显恩爱
```

##使用说明




