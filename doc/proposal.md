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
###NLP 任务的解决过程

1. 基于tokenization.py脚本中的Tokenizer对输入的句子进行token化，即按字粒度对句子进行切分；
2. 分类标志符号[CLS]与token化后的句子拼接在一起作为ERNIE模型的输入，经过 ERNIE 前向计算后得到每个token对应的embedding向量表示；
3. 在单句分类任务中，[CLS]位置对应的嵌入式向量会用来作为分类特征。只需将[CLS]对应的embedding抽取出来，再经过一个全连接层得到分类的 logits 值，最后经过softmax归一化后与训练数据中的label一起计算交叉熵，就得到了优化的损失函数；
4. 经过几轮的fine-tuning，就可以训练出解决具体任务的ERNIE模型。


[simple-case代码及简易教程](https://aistudio.baidu.com/aistudio/projectdetail/874233)

###运行除ernie-with-jina的dockerfile外所需额外环境：

```pip install vim```

```pip install wget```

```pip install sklearn```

```wget https://ernie-github.cdn.bcebos.com/data-chnsenticorp.tar.gz```

```tar xvf data-chnsenticorp.tar.gz```

运行示例程序会下载 ```https://ernie-github.cdn.bcebos.com/model-ernie1.0.1.tar.gz```。 若下载失败，手动 ```wget https://ernie-github.cdn.bcebos.com/model-ernie1.0.1.tar.gz``` 随后解压并移至目标目录。

## BERT（Bidirectional Encoder Representations from Transformers）

### natural language processing tasks:

1. sentence-level tasks such as natural language inference and paraphrasing, which aim to predict the relationships between sentences by analyzing them holistically
2. token-level tasks such as named entity recognition and question answering, where models are required to produce ﬁne-grained output at the token level

### two existing strategies for applying pre-trained language representations to downstream tasks: 

1. feature-based: such as ELMo, uses task-speciﬁc architectures that include the pre-trained representations as additional features 
2. ﬁne-tuning: such as the Generative Pre-trained Transformer, introduces minimal task-speciﬁc parameters, and is trained on the downstream tasks by simply ﬁne-tuning all pretrained parameters

The two approaches share the same objective function during pre-training, where they use unidirectional language models to learn general language representations.

BERT alleviates the previously mentioned unidirectionality constraint by using a “masked language model” (MLM) pre-training objective, inspired by the Cloze task (Taylor, 1953). The masked language model randomly masks some of the tokens from the input, and the objective is to predict the original vocabulary id of the masked word based only on its context.

There are two steps in BERT framework: pre-training and ﬁne-tuning. During pre-training, the model is trained on unlabeled data over different pre-training tasks. For ﬁnetuning, the BERT model is ﬁrst initialized with the pre-trained parameters, and all of the parameters are ﬁne-tuned using labeled data from the downstream tasks. Each downstream task has separate ﬁne-tuned models, even though they are initialized with the same pre-trained parameters.

## X as service

```
from jina.flow import Flow

f = (Flow(callback_on_body=True)
     .add(name='spit', uses='Sentencizer')
     .add(name='encode', uses='jinaai/hub.executors.encoders.nlp.transformers-pytorch',
          parallel=2, timeout_ready=20000))

```
1. What is transformers

	"Griezmann", "his", "Frenchman" can be pointed as one person in a paragraph. Capturing such relationships and sequence of words in sentences is vital for a machine to understand a natural language. This is where the Transformer concept plays a major role.

	1. Sequence-to-Sequence Models – A Backdrop
		
		convert sequences of Type A to sequences of Type B. For example, translation of English sentences to German sentences is a sequence-to-sequence task.
		
	2. Recurrent Neural Network (RNN) based sequence-to-sequence models
		（1）Both Encoder and Decoder are RNNs
		（2）At every time step in the Encoder, the RNN takes a word vector (xi) from the input sequence and a hidden state (Hi) from the previous time step
		（3）The hidden state is updated at each time step
		（4）The hidden state from the last unit is known as the context vector. This contains information about the input sequence
	
	The Transformer in NLP is a novel architecture that aims to solve sequence-to-sequence tasks while handling long-range dependencies with ease.
	
	
2. What is ```jinaai/hub.executors.encoders.nlp.transformers-pytorch``` and how to change it.
	
	[url is here](https://www.analyticsvidhya.com/blog/2019/07/pytorch-transformers-nlp-python/?utm_source=blog&utm_medium=7-innovative-machine-learning-github-projects-in-python)

	'I have taken this p from PyTorch-Transformers’ documentation. This library currently contains PyTorch implementations, pre-trained model weights, usage scripts and conversion utilities for the following models:

	BERT (from Google) released with the paper BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

	GPT (from OpenAI) released with the paper Improving Language Understanding by Generative Pre-Training

	GPT-2 (from OpenAI) released with the paper Language Models are Unsupervised Multitask Learners

	Transformer-XL (from Google/CMU) released with the paper Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context

	XLNet (from Google/CMU) released with the paper XLNet: Generalized Autoregressive Pretraining for Language Understanding

	XLM (from Facebook) released together with the paper Cross-lingual Language Model Pretraining

	All of the above models are the best in class for various NLP tasks. Some of these models are as recent as the previous month!

	Most of the State-of-the-Art models require tons of training data and days of training on expensive GPU hardware which is something only the big technology companies and research labs can afford. But with the launch of PyTorch-Transformers, now anyone can utilize the power of State-of-the-Art models!'
	
## Jina
### Document & Chunk

1. a Document is anything that you want to search for

2. a Chunk is a small semantic unit of a Document

### YAML config 

A YAML config is widely used in Jina to describe the properties of an object.

### Executor

Executor represents an algorithmic unit in Jina.

### Driver

Driver defines how an Executor behaves on network requests.

### Pea

Pea wraps an Executor and grants it the ability to exchange data over a network. 

### Pod

Pod is a group of Peas with the same property. 

### Flow

Flow represents a high-level task,

```
f = (Flow().add(name='p1')
           .add(name='p2', image='jinaai/hub.executors.encoders.bidaf:latest')
           .add(name='p3'))
```
p2 is running in a container


### 跑通xx-as-service的example
代码如下

``` 
from jina.flow import Flow

f = (Flow(callback_on_body=True)
     .add(name='spit', uses='Sentencizer')
     .add(name='encode', uses='enc.yml',
          parallel=2, timeout_ready=20000))
```

```enc.yml```
为

```
!TransformerTorchEncoder
with:
  pooling_strategy: cls
  model_name: distilbert-base-cased
  max_length: 96
```

```
def input_fn():
    with open('README.md') as fp:
        for v in fp:
            yield v.encode()
```
```
def print_embed(req):
    for d in req.docs:
        for c in d.chunks:
            embed = pb2array(c.embedding)
            text = colored(f'{c.text[:10]}...' if len(c.text) > 10 else c.text, 'blue')
            print(f'{text} embed to {embed.shape} [{embed[0]:.3f}, {embed[1]:.3f}...]')
```
```
with f:
    f.index(input_fn, batch_size=32, callback=print_embed)

```
需安装的依赖有:

``` pip install transformers```

``` pip install torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple```


