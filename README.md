TextRank4ZH

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

关于模块版本，以下作为参考：

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




##测试

`test.py`提供了使用的示例。

##使用说明




