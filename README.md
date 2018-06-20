## 使用神经网络和NLP技术实现的高中物理知识点分类

在实现过程中主要参考了[这篇文章](https://www.leiphone.com/news/201705/4CFBFH5szAubNQiK.html

**预处理**

首先将知识树中所有的知识点进行预处理，根据不同的知识点类别进行分类，将该二级知识点所有的叶子节点放到同一个txt文档里。

**分词**

对txt文档进行分词处理，提取有意义的关键词。

**生成词典**

根据词频（TF）和逆文档频率（IDF）来衡量词汇在文章中的重要程度，得到词典

**生成词袋**

实现向量化文本，利用生成的词典，将文本转换为向量

