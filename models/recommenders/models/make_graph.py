import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


def graph_output(path):
    df = pd.read_csv(path, delimiter=',', header=None)

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

    return loss, acc, hit_ratio, ndcg


loss_8, acc_8, hit_ratio_8, ndcg_8 = graph_output('8factor_graph_neumf_10_recipe.csv')
loss_128, acc_128, hit_ratio_128, ndcg_128 = graph_output('128facter_graph_neumf_small_recipe.csv')

epochs = np.arange(0, 20, 1)

# print(loss)
# print(acc)
# print(hit_ratio)
# print(ndcg)

plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.plot(epochs, loss_8, 'b', label='8factor')
plt.plot(epochs, loss_8, 'r', label='64factor')
plt.plot(epochs, loss_128, 'g', label='128factor')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.subplot(2, 2, 2)
plt.plot(epochs, acc_8, 'b', label='8factor')
plt.plot(epochs, acc_8, 'r', label='64factor')
plt.plot(epochs, acc_128, 'g', label='128factor')
plt.xlabel('epochs')
plt.ylabel('acc')
plt.legend()
plt.subplot(2, 2, 3)
plt.plot(epochs, hit_ratio_8, 'b', label='8factor')
plt.plot(epochs, hit_ratio_8, 'r', label='64factor')
plt.plot(epochs, hit_ratio_128, 'g', label='128factor')
plt.xlabel('epochs')
plt.ylabel('hit_ratio')
plt.legend()
plt.subplot(2, 2, 4)
plt.plot(epochs, ndcg_8, 'b', label='8factor')
plt.plot(epochs, ndcg_8, 'r', label='64factor')
plt.plot(epochs, ndcg_128, 'g', label='128factor')
plt.xlabel('epochs')
plt.ylabel('ndcg')
plt.legend()

plt.show()

