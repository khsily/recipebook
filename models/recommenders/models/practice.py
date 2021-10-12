# practice.py
import json

import tensorflow as tf
import numpy as np
import pandas as pd
import random
import pprint
from evaluate import evaluate_model
import GMF
import re


def test_small_data():
    food_name = [
        '짜장면', '탕수육', '짬뽕', '유린기', '볶음밥', '깐쇼새우', '떡볶이', '오뎅탕', '김치볶음밥', '김밥',
        '라면', '우동', '잔치국수', '후라이드치킨', '피자', '양념치킨', '토마토 파스타', '까르보나라', '알리오올리오', '봉골레 파스타',
        '크림 파스타', '크림 리조또', '토마토 리조또', '치킨 샐러드', '샌드위치', '리코타 치즈 샐러드', '발사믹 토마토 샐러드', '단호박 샐러드', '닭가슴살 샐러드', '양배추 샐러드'
    ]

    id_name_food = ['짜장면', '김밥', '토마토 파스타', '후라이드치킨', '닭가슴살 샐러드']

    k = 1
    id = {}
    for i in range(len(id_name_food)):
        pair = [(id_name_food[i], j) for j in id_name_food[:i] if j != id_name_food[i]]
        for idx1, idx2 in pair:
            id[k] = (idx1, idx2)
            k += 1

    for i in range(len(id_name_food)):
        if i + 1 < len(id_name_food):
            for j in id_name_food[:i]:
                if len([id_name_food[i], id_name_food[i + 1], j]) > 2:
                    id[k] = (id_name_food[i], id_name_food[i + 1], j)
                    k += 1

    model = tf.keras.models.load_model('test_model.h5')

    df = pd.read_csv('D:/python/tensorflow2.5/project_ratatouiille/data/test.test', delimiter='|', header=None, names=['user_id', 'item_id'])
    userid = df['user_id'].values
    itemid = df['item_id'].values

    preds = model.predict([userid, itemid])

    print(id[1])

    rating = {}
    for n, r in zip(food_name, preds):
        rating[float(r)] = n

    for i in reversed(sorted(list(rating.keys()))):
        print(rating[i], i)


def test_GMF(path):
    model = tf.keras.models.load_model(path)
    testRatings, testNegatives, topK, evaluation_threads = \
        GMF.testRatings, GMF.testNegatives, GMF.topK, GMF.evaluation_threads
    (hits, ndcgs) = evaluate_model(model, testRatings, testNegatives, topK, evaluation_threads)
    hr, ndcg = np.array(hits).mean(), np.array(ndcgs).mean()
    print('HR = %.4f, NDCG = %.4f' % (hr, ndcg))


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

# test_GMF('Pretrain/recipe_GMF_8_1633923387.h5')


user_idx, user_list = get_data('D:\python\\tensorflow2.5\project_ratatouiille\data\idx_id.csv')
item_idx, item_list = get_data('D:\python\\tensorflow2.5\project_ratatouiille\data\idx_item.csv')
theme, item = get_data('D:\python\\tensorflow2.5\project_ratatouiille\data\\theme_item.csv')

idx2id = {i: u for i, u in zip(user_idx, user_list)}
id2idx = {u: i for i, u in zip(user_idx, user_list)}
idx2item = {i: u for i, u in zip(item_idx, item_list)}
item2idx = {u: i for i, u in zip(item_idx, item_list)}

# print(idx2id)
# print(idx2item)

category_name = ['한식', '양식', '일식', '중식', '퓨전', '분식', '다이어트']

theme_item, item_list = {}, []
for c in category_name:
    for t, i in zip(theme, item):
        if t == c:
            item_list.append(i)
    theme_item[c] = item_list
    item_list = []

# print(theme_item)

random.seed(100)

test_id = random.choice(user_idx)

user_id, item_id = [], []
for i in theme_item['퓨전']:
    user_id.append(test_id)
    item_id.append(item2idx[i])

user_id, item_id = np.array(user_id, dtype=np.int32), np.array(item_id, dtype=np.int32)

model = tf.keras.models.load_model('test_model.h5')
preds = model.predict([user_id, item_id])

predictions = []
for u, i, p in zip(user_id, item_id, preds):
    u, i, p = str(u), str(i), float(p)
    predictions.append([idx2id[u], idx2item[i], p])

pprint.pprint(sorted(predictions, reverse=True, key=lambda x: x[2]))


