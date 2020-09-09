import sys
sys.path.append('./ERNIE')
import numpy as np
from sklearn.metrics import f1_score
import paddle as P
import paddle.fluid as F
import paddle.fluid.layers as L
import paddle.fluid.dygraph as D

from ernie.tokenizing_ernie import ErnieTokenizer
from ernie.modeling_ernie import ErnieModelForSequenceClassification

BATCH=32
MAX_SEQLEN=300
LR=5e-5
EPOCH=10

D.guard().__enter__()

ernie = ErnieModelForSequenceClassification.from_pretrained('ernie-1.0', num_labels=3)
optimizer = F.optimizer.Adam(LR, parameter_list=ernie.parameters())
tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')

def make_data(path):
    data = []
    for i, l in enumerate(open(path)):
        if i == 0:
            continue
        l = l.strip().split('\t')
        text, label = l[0], int(l[1])
        text_id, _ = tokenizer.encode(text)
        text_id = text_id[:MAX_SEQLEN]
        text_id = np.pad(text_id, [0, MAX_SEQLEN-len(text_id)], mode='constant')
        label_id = np.array(label+1)
        data.append((text_id, label_id))
    return data

train_data = make_data('./chnsenticorp/train/part.0')
test_data = make_data('./chnsenticorp/dev/part.0')

def get_batch_data(data, i):
    d = data[i*BATCH: (i + 1) * BATCH]
    feature, label = zip(*d)
    feature = np.stack(feature) 
    label = np.stack(list(label))
    feature = D.to_variable(feature)
    label = D.to_variable(label)
    return feature, label

for i in range(EPOCH):
    np.random.shuffle(train_data)
    #train
    for j in range(len(train_data) // BATCH):
        feature, label = get_batch_data(train_data, j)
        loss, _ = ernie(feature, labels=label)
        loss.backward()
        optimizer.minimize(loss)
        ernie.clear_gradients()
        if j % 10 == 0:
            print('train %d: loss %.5f' % (j, loss.numpy()))
        # evaluate
        if j % 100 == 0:
            all_pred, all_label = [], []
            with D.base._switch_tracer_mode_guard_(is_train=False): 
                ernie.eval()
                for j in range(len(test_data) // BATCH):
                    feature, label = get_batch_data(test_data, j)
                    loss, logits = ernie(feature, labels=label)
                    all_pred.extend(L.argmax(logits, -1).numpy())
                    all_label.extend(label.numpy())
                ernie.train()
            f1 = f1_score(all_label, all_pred, average='macro')
            acc = (np.array(all_label) == np.array(all_pred)).astype(np.float32).mean()
            print('acc %.5f' % acc)
