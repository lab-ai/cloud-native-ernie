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



