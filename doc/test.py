import numpy as np
import paddle.fluid.dygraph as D
from ernie.tokenizing_ernie import ErnieTokenizer
from ernie.modeling_ernie import ErnieModel

D.guard().__enter__() # activate paddle `dygrpah` mode

model = ErnieModel.from_pretrained('ernie-1.0')    # Try to get pretrained model from server, make sure you have network connection
# model.eval()是去掉训练过程（也就是没有了反向计算过程），只是测试
model.eval() #加载模型并将模型的状态设置为校验状态（eval），显式告诉框架我们接下来只会使用前向计算的流程，不会计算梯度和梯度反向传播，这将减少内存的消耗。
tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')

ids, _ = tokenizer.encode('hello world')
ids = D.to_variable(np.expand_dims(ids, 0))  # insert extra `batch` dimension
pooled, encoded = model(ids)                 # eager execution
print(pooled.numpy())                        # convert  results to numpy
