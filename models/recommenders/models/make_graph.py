import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


df = pd.read_csv('64factor_graph.csv', delimiter=',', header=None)

# for i in range(4):
#     print(df[i])

loss, acc = [], []
for l, a in zip(df[0], df[1]):
    loss.append(float(re.findall(r'\[(.+?)\]', l)[0]))
    acc.append(float(re.findall(r'\[(.+?)\]', a)[0]))

hit_ratio, ndcg = [], []
for h, n in zip(df[2], df[3]):
    hit_ratio.append(float(h.split()[1]))
    ndcg.append(float(n.split()[1]))

epochs = np.arange(0, 20, 1)

# print(loss)
# print(acc)
# print(hit_ratio)
# print(ndcg)

plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.plot(epochs, loss, 'r')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.subplot(2, 2, 2)
plt.plot(epochs, acc, 'b')
plt.xlabel('epochs')
plt.ylabel('acc')
plt.subplot(2, 2, 3)
plt.plot(epochs, hit_ratio, 'm')
plt.xlabel('epochs')
plt.ylabel('hit_ratio')
plt.subplot(2, 2, 4)
plt.plot(epochs, ndcg, 'g')
plt.xlabel('epochs')
plt.ylabel('ndcg')

plt.show()

