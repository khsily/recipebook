# prediction.py
import tensorflow as tf
import numpy as np
import pandas as pd
import random
import pprint
import re
import math
import collections


def get_data(path):
    f = open(path, 'r', encoding='utf-8')
    rows = f.readlines()
    num, item = [], []
    for row in rows:
        row = re.sub(r'\n', '', row)
        num.append(row.split('|')[0])
        item.append(row.split('|')[1])

    f.close()

    return num, item


def make_idx2_st(idx, st):
    idx2st = {i: u for i, u in zip(idx, st)}
    st2idx = {u: i for i, u in zip(idx, st)}

    return idx2st, st2idx


def theme_dic(category_name, theme, item):
    theme_item, item_list = {}, []
    for c in category_name:
        for t, i in zip(theme, item):
            i = i.strip()
            if t == c:
                item_list.append(i)
        theme_item[c] = item_list
        item_list = []

    return theme_item


def predictions(theme_item, test_id, choose_category, model_path, item2idx):
    user_id, item_id = [], []
    for i in choose_category:
        for j in theme_item[i]:
            user_id.append(test_id)
            item_id.append(item2idx[j])

    item_id = list(set(item_id))
    user_id = user_id[:len(item_id)]
    user_id, item_id = np.array(user_id, dtype=np.int32), np.array(item_id, dtype=np.int32)

    model = tf.keras.models.load_model(model_path)
    preds = model.predict([user_id, item_id])

    predictions = []
    for u, i, p in zip(user_id, item_id, preds):
        u, i, p = str(u), str(i), float(p)
        predictions.append([i, p])

    predictions = sorted(predictions, reverse=True, key=lambda x: x[1])
    recommends = [p[0] for p in predictions[:20]]

    return recommends


if __name__ == '__main__':
    idx_id_path = 'data/idx_id.csv'
    idx_item_path = 'data/idx_item.csv'
    theme_item = 'data\\theme_item.csv'

    user_idx, user_list = get_data(idx_id_path)
    item_idx, item_list = get_data(idx_item_path)
    item_list = [i.strip() for i in item_list]

    theme, item = get_data(theme_item)

    idx2id, id2idx = make_idx2_st(user_idx, user_list)
    idx2item, item2idx = make_idx2_st(item_idx, item_list)

    category_name = ['한식', '양식', '일식', '중식', '퓨전', '분식', '다이어트']

    theme_item = theme_dic(category_name, theme, item)

    # random.seed(30)
    test_id = random.choice(user_idx)                   # input user_idx
    print(test_id)
    print(idx2id[test_id])
    choose_category = ['한식', '양식', '일식', '중식', '퓨전', '분식', '다이어트']       # input category

    model_path = 'recipe_test_model.h5'

    recommends_top10 = predictions(theme_item, test_id, choose_category, model_path, item2idx)

    # print([idx2item[i] for i in recommends_top10])

f = open('data/recipe.train.rating', 'r', encoding='utf-8')
item, evaluate = [], []
for i in f.readlines():
    i = i.split('\t')
    if i[0] == test_id:
        item.append(i[1])
        evaluate.append((i[1], int(i[2])))

f.close()
print(collections.Counter(item).most_common())
item = [i[0] for i in collections.Counter(item).most_common(20)]

print(item)
item = [idx2item[i] for i in item]
preds = [idx2item[i] for i in recommends_top10]

for i, p in zip(item, preds):
    print(i, '\t\t|', p)

hr = 0
for i in preds:
    if i in item:
        hr += 1
        # print(i)

dcg, idcg = 0, 0
for i in range(len(item)):
    idcg += 1 / math.log(i + 2)
    if item[i] in preds:
        dcg += 1 / math.log(i + 2)
        print(i)

print(dcg, idcg)
ndcg = dcg / idcg

print(hr, ndcg)






