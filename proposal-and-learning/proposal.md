# Propoasal
## Docker
常用指令

1. 查看本地镜像 ```docker images```
2. 创建容器 ```docker run -dit --name=容器名 镜像id /bin/bash ```
3. 查看所有的容器 ```docker ps -a```
4. 进入容器 ```docker exec -it 容器名 /bin/bash·```
5. 退出容器 ```exit```
6. 将容器制作成镜像 ```docker  commit  -m  '镜像描述'  -a  '制作者'  容器名  镜像名```
7. 将制作好的镜像打成 tar 包 ```docker  save  -o  tar包的名字  镜像名```
8. 根据Dockerfile创建容器 ```docker build -t nginx:v1 .```
9. 本地上传文件 ```docker inspect -f '{{.ID}}' 容器名``` ```docker cp 本地路径 容器长ID:容器路径```

[参考链接1](https://www.cnblogs.com/pjcd-32718195/p/11762079.html)
[参考链接2](https://www.cnblogs.com/ityouknow/p/8588725.html)
[参考链接3](https://blog.csdn.net/xbw12138/article/details/79126396)
 
## Ernie
NLP 任务的解决过程

1. 基于tokenization.py脚本中的Tokenizer对输入的句子进行token化，即按字粒度对句子进行切分；
2. 分类标志符号[CLS]与token化后的句子拼接在一起作为ERNIE模型的输入，经过 ERNIE 前向计算后得到每个token对应的embedding向量表示；
3. 在单句分类任务中，[CLS]位置对应的嵌入式向量会用来作为分类特征。只需将[CLS]对应的embedding抽取出来，再经过一个全连接层得到分类的 logits 值，最后经过softmax归一化后与训练数据中的label一起计算交叉熵，就得到了优化的损失函数；
4. 经过几轮的fine-tuning，就可以训练出解决具体任务的ERNIE模型。


[simple-case代码及简易教程](https://aistudio.baidu.com/aistudio/projectdetail/874233)

运行除ernie-with-jina的dockerfile外所需额外环境：

```pip install vim```

```pip install wget```

```pip install sklearn```

```wget https://ernie-github.cdn.bcebos.com/data-chnsenticorp.tar.gz```

```tar xvf data-chnsenticorp.tar.gz```

运行示例程序会下载 ```https://ernie-github.cdn.bcebos.com/model-ernie1.0.1.tar.gz```。 若下载失败，手动 ```wget https://ernie-github.cdn.bcebos.com/model-ernie1.0.1.tar.gz``` 随后解压并移至目标目录。

## BERT（Bidirectional Encoder Representations from Transformers）

natural language processing tasks:

1. sentence-level tasks such as natural language inference and paraphrasing, which aim to predict the relationships between sentences by analyzing them holistically
2. token-level tasks such as named entity recognition and question answering, where models are required to produce ﬁne-grained output at the token level

two existing strategies for applying pre-trained language representations to downstream tasks: 

1. feature-based: such as ELMo, uses task-speciﬁc architectures that include the pre-trained representations as additional features 
2. ﬁne-tuning: such as the Generative Pre-trained Transformer, introduces minimal task-speciﬁc parameters, and is trained on the downstream tasks by simply ﬁne-tuning all pretrained parameters

The two approaches share the same objective function during pre-training, where they use unidirectional language models to learn general language representations.