# Paddle-learning

## Paddlehub-learning

### PaddleHub预训练模型LAC完成词法分析

```python
import paddlehub as hub

with open("test.txt", 'r') as f:
    test_text = []
    for line in f:
        test_text.append(line.strip())
print(test_text)

module = hub.Module(name="lac")


results = module.lexical_analysis(texts=test_text)

for result in results:
    print(result)
```

## 用PaddlePaddle实现BERT

## 模型综述

BERT不是在给定所有前面词的条件下预测最可能的当前词，而是随机遮掩一些词，并利用所有没被遮掩的词进行预测。 因此BERT的任务主要有以下两个：

1. 二分类任务：在数据集中抽取两个句子A和B，B有50%的概率是A的下一句，这样通过判断B是否是A的下一句来判断BERT模型
2. Mask预测任务：传统语言模型是给定所有前面词来预测最可能的当前词，而BERT模型则是随机的使用「mask」来掩盖一些词，并利用所有没有被掩盖的词对这些词进行预测。论文中是随机mask掉15%的词，并且在确定需要mask的词后，80%的情况会使用「mask」来掩盖，10%的情况会使用随机词来替换，10%的情况会保留原词，

## 文件结构

````
|-- model				# 用于存放model文件
|-- |-- classifier.py			# 使用bert模型进行分类任务的模型
|-- |-- bert.py				# bert模型
|-- |-- transformer_encoder.py		# transformer模型的encoder部分，bert是基于该网络进行的
|-- utils				# 工具模块
|-- |-- init.py				# 精度转换、加载参数等方法
|-- |-- cards.py			# 获取gpu的数量
|-- |-- args.py				# 初始化args、输出args等方法
|-- |-- fp16.py				# 用于精度为fp16的训练
|-- tokenization.py			# 用于预处理数据，例如：token化
|-- run_squad.py			# 使用bert在SQuAD数据集上进行阅读理解的训练和预测
|-- optimization.py			# 学习率衰减方式和优化器设置
|-- dist_utils.py			# 通用函数
|-- train.py				# bert模型的训练脚本，当do_test参数为True时可以进行测试
|-- batching.py				# 生成一个batch的数据，同时进行了mask操作
|-- convert_params.py			# 将谷歌官方的bert模型转化为paddle的模型
|-- run_classifier.py			# 使用bert模型进行语句和语句对分类的Fine-tuning
|-- predict_classifier.py		# 使用Fine-tuning后的模型语句对分类模型进行预测并将参数固化
|-- infer_classifier.py			# 使用固化的参数进行语句对分类
|-- test_local_dist.sh			# 在本地模拟分布式训练的样例
|-- train.sh				# 训练脚本
|-- XNLI_train.sh			# 语句对分类任务的训练脚本
|-- train_use_fp16.sh			# 使用fp16精度进行训练的脚本
````

## BERT 预训练

### BERT in PaddlePaddle

```train.py```

1. ```paddle.fluid.layers.py_reader(capacity, shapes, dtypes, lod_levels=None, name=None, use_double_buffer=True)``` 创建一个在Python端提供数据的reader。该Reader提供了 `decorate_paddle_reader()` 和 `decorate_tensor_provider()` 来设置Python generator作为数据源，将数据源中的数据feed到Reader Variable。[参考链接](https://www.paddlepaddle.org.cn/documentation/docs/zh/api_cn/layers_cn/py_reader_cn.html#paddle.fluid.layers.py_reader)

2. ```paddle.fluid.layers.read_file(reader)``` 从给定的reader中读取数据

   reader是一个Variable，它可以是由函数fluid.layers.py_reader()生成的reader，或者是由函数fluid.layers.double_buffer()生成的装饰Variable。[参考链接](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.7/api_cn/layers_cn/read_file_cn.html)

3. ``` class paddle.fluid.executor.Executor(place)``` 执行引擎（Executor）使用python脚本驱动，支持在单/多GPU、单/多CPU环境下运行。 Python Executor可以接收传入的program,并根据feed map(输入映射表)和fetch_list(结果获取表) 向program中添加feed operators(数据输入算子)和fetch operators（结果获取算子)。 feed map为该program提供输入数据。fetch_list提供program训练结束后用户预期的变量（或识别类场景中的命名）。

   应注意，执行器会执行program中的所有算子而不仅仅是依赖于fetch_list的那部分。

   Executor将全局变量存储到全局作用域中，并为临时变量创建局部作用域。 当每一mini-batch上的前向/反向运算完成后，局部作用域的内容将被废弃， 但全局作用域中的变量将在Executor的不同执行过程中一直存在。[参考链接](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.5/api_cn/executor_cn.html)

3. ```class paddle.fluid.Program``` **默认情况下，Paddle Fluid内部默认含有** [default_startup_program](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.8/api_cn/fluid_cn/default_startup_program_cn.html#cn-api-fluid-default-startup-program) **和** [default_main_program](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.8/api_cn/fluid_cn/default_main_program_cn.html#cn-api-fluid-default-main-program) **，它们共享参数。** [default_startup_program](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.8/api_cn/fluid_cn/default_startup_program_cn.html#cn-api-fluid-default-startup-program) **只运行一次来初始化参数，** [default_main_program](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.8/api_cn/fluid_cn/default_main_program_cn.html#cn-api-fluid-default-main-program) **在每个mini batch中运行并更新权重。**Program是Paddle Fluid对于计算图的一种静态描述。[参考链接](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.8/api_cn/fluid_cn/Program_cn.html)
4. ```paddle.fluid.program_guard(main_program, startup_program=None)```

程序逻辑：

```main```->```train(args)```

```train(args)```:

1. Get bert_config

2. Set train_program and startup_program -> create model with bert config

3. Set test_program -> create model with bert config

4. create model: 

   1. Set ```fluid.layers.py_reader```
   2. Set ```fluid.layers.read_file```
   3. Set and get BertModel
   4. ```bert.get_pretraining_output```

5. ```
   exe = fluid.Executor(place)
   exe.run(startup_prog)
   ```

6. Use DataReader to get data

7. Start training

### BERT-pytorch

```
|-- __init__.py
|-- __main__.py
|-- trainer
|-- |-- __init__.py
|-- |-- optim_schedule.py
|-- |-- pretrain.py
|-- model
|-- |-- attention
|-- |-- |-- __init__.py
|-- |-- |-- multi_head.py
|-- |-- |-- single.py
|-- |-- embedding
|-- |-- |-- __init__.py
|-- |-- |-- bert.py
|-- |-- |-- position.py
|-- |-- |-- segment.py
|-- |-- |-- token.py
|-- |-- utils
|-- |-- |-- __init__.py
|-- |-- |-- feed_forward.py
|-- |-- |-- gelu.py
|-- |-- |-- layer_norm.py
|-- |-- |-- sublayer.py
|-- |-- __init__.py
|-- |-- bert.py
|-- |-- language_model.py
|-- |-- transformer.py
|-- dataset
|-- |-- __init__.py
|-- |-- dataset.py
|-- |-- vocab.py
```



```__main__.py```

1. Set bert
2. Set trainer
3. trainer.train()

```model/bert.py``` (model)

1. x -> mask
2. x + segment_info -> x (embedding)
3. x + mask -> x (transformer)
4. return x

```model/transformer.py``` (model)

1. _x -> _x (MultiHeadedAttention)
2. x + _x -> x (SublayerConnection)
3. x + PositionwiseFeedForward -> x (SublayerConnection)
4. x -> x (dropout)
5. return x

```model/language_model.py``` 

(BERTLM)

1. x + segment_laebel -> x (bert)
2. x -> tmp1 (NextSentencePrediction); x -> tmp2 (MaskedLanguageModel)
3. return tmp1, tmp2

(NextSentencePrediction)

1. x[:, 0] -> tmp1 (linear)
2. tmp1 -> tmp2 (softmax)
3. return tmp2

(MaskedLanguageModel)

1. x -> x (linear)
2. x -> x (softmax)
3. return x

```model/embedding/bert.py``` (model)

1. sequence -> tmp1 (TokenEmbedding)
2. sequence -> tmp2 (PositionalEmbedding)
3. segment_label -> tmp3 (SegmentEmbedding)
4. Tmp1 + tmp2 + tmp3 -> x
5. x -> x (dropout)
6. return x

```model/embedding/position.py``` (PositionEmbedding)

1. ```python
   pe = torch.zeros(max_len, d_model).float()
   pe.require_grad = False
   
   position = torch.arange(0, max_len).float().unsqueeze(1)
   div_term = (torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model)).exp()
   
   pe[:, 0::2] = torch.sin(position * div_term)
   pe[:, 1::2] = torch.cos(position * div_term)
   
   pe = pe.unsqueeze(0)
   ```

2. return pe[max_len, x.size(1)]

```model/embedding/segment.py``` (SegmentEmbedding)

```model/embedding/token.py``` (PositionEmbedding)

```model/attention/single.py``` (Attention)

1. 

```model/attention/multi_head.py``` (MultiHeadedAttention)

1. 

```model/utils/feed_forward.py``` (PositionwiseFeedForward)

1. x -> tmp1 (Linear)
2. tmp1 -> tmp2 (GELU)
3. tmp2 -> tmp3 (dropout)
4. tmp3 -> tmp4 (Linear)
5. return tmp4

```model/utils/gelu.py``` (GELU)

1. ```python
   def forward(self, x):
     return 0.5 * x * (1 + torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * torch.pow(x, 3))))
   ```

```model/utils/layer_norm.py``` (LayerNorm)

1. ```python
   def forward(self, x):
     mean = x.mean(-1, keepdim=True)
     std = x.std(-1, keepdim=True)
     return self.a_2 * (x - mean) / (std + self.eps) + self.b_2
   ```

```model/utils/sublayer.py``` (SublayerConnection)

1. x -> tmp1 (LayerNorm)
2. tmp1 -> tmp2 (sublayer)
3. tmp2 -> tmp3 (dropout)
4. return x + tmp3

```train/optim_schedule.py```

This file is to set the optimization

```train/pretrain.py```

This file is for training details.

# 对话情绪识别 



对话情绪类别有三种：负向情绪(0)、中性情绪(1)和正向情绪(2)，属于短文本三分类问题。

# Paddle-Serving

## Installation

```
docker pull hub.baidubce.com/paddlepaddle/serving:latest
docker run -p 9292:9292 --name paddle-serving-test -dit	hub.baidubce.com/paddlepaddle/serving:latest
docker exec -it paddle-serving-test bash
pip install paddle-serving-server==0.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Test

```
wget --no-check-certificate https://paddle-serving.bj.bcebos.com/uci_housing.tar.gz
tar -xzf uci_housing.tar.gz
python -m paddle_serving_server.serve --model uci_housing_model --thread 10 --port 9292 --name uci
```

```
curl -H "Content-Type:application/json" -X POST -d '{"feed":[{"x": [0.0137, -0.1136, 0.2553, -0.0692, 0.0582, -0.0727, -0.1583, -0.0584, 0.6283, 0.4919, 0.1856, 0.0795, -0.0332]}], "fetch":["price"]}' http://127.0.0.1:9292/uci/prediction
```

## An End-to-end Tutorial from Training to Inference Service Deployment



## Paddle Serving服务化部署框架

常见的深度学习模型开发流程需要经过问题定义、数据准备、特征提取、建模、训练过程，以及最后一个环——将训练出来的模型部署应用到实际业务中。

- 模型服务化部署：将模型以线上服务的形式部署在服务器或者云端，用户通过客户端请求发送需要推理的输入内容，服务器或者云通过响应报文将推理结果返回给用户。

### 部署在线推理服务进阶流程

所谓进阶流程，其实还是那三个步骤，获取可用于部署的在线服务的模型、启动服务端和使用客户端访问服务端进行推理。

#### 获取可用于部署在线服务的模型

#### 启动推理服务

Paddle Serving框架支持两种推理服务方式，分别是**RPC服务**和**Web服务**，用户可以任选其一：

1. RPC服务是CS架构，用户使用客户端来访问服务端获取推理结果，客户端和服务端之间的通信使用的是百度开源的一款RPC通信库来完成的。
2. Web服务是BS架构，用户可以使用浏览器或其它Web应用通过HTTP协议访问服务端。与RPC相比其优势在于可以适用于包括Linux操作系统在内的不同系统环境。

