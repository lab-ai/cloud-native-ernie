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

```train.py```

1. ```paddle.fluid.layers.py_reader(capacity, shapes, dtypes, lod_levels=None, name=None, use_double_buffer=True)``` 创建一个在Python端提供数据的reader。该Reader提供了 `decorate_paddle_reader()` 和 `decorate_tensor_provider()` 来设置Python generator作为数据源，将数据源中的数据feed到Reader Variable。[参考链接](https://www.paddlepaddle.org.cn/documentation/docs/zh/api_cn/layers_cn/py_reader_cn.html#paddle.fluid.layers.py_reader)

2. ``` class paddle.fluid.executor.Executor(place)``` 执行引擎（Executor）使用python脚本驱动，支持在单/多GPU、单/多CPU环境下运行。 Python Executor可以接收传入的program,并根据feed map(输入映射表)和fetch_list(结果获取表) 向program中添加feed operators(数据输入算子)和fetch operators（结果获取算子)。 feed map为该program提供输入数据。fetch_list提供program训练结束后用户预期的变量（或识别类场景中的命名）。

   应注意，执行器会执行program中的所有算子而不仅仅是依赖于fetch_list的那部分。

   Executor将全局变量存储到全局作用域中，并为临时变量创建局部作用域。 当每一mini-batch上的前向/反向运算完成后，局部作用域的内容将被废弃， 但全局作用域中的变量将在Executor的不同执行过程中一直存在。[参考链接](https://www.paddlepaddle.org.cn/documentation/docs/zh/1.5/api_cn/executor_cn.html)

