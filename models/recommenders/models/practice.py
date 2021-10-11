# practice.py
import json

import tensorflow as tf
import numpy as np
import pandas as pd
import random
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


# test_GMF('Pretrain/recipe_GMF_8_1633923387.h5')

with open('D:\python\\tensorflow2.5\project_ratatouiille\data\id_idx.csv', 'r', encoding='utf-8') as f:
    data = re.sub(r'[\[\]\n\s]', '', f.readlines()[0])
    user_list = data.split(',')
    # print(user_id)

with open('D:\python\\tensorflow2.5\project_ratatouiille\data\item_idx.csv', 'r', encoding='utf-8') as f:
    data = re.sub(r'[\[\]\n\s]', '', f.readlines()[0])
    item_list = data.split(',')
    # print(item_id)

with open('D:\python\\tensorflow2.5\project_ratatouiille\data\idx2id.json', 'r', encoding='utf-8') as f:
    idx2id = json.load(f)
    # print(idx2id)

with open('D:\python\\tensorflow2.5\project_ratatouiille\data\idx2item.json', 'r', encoding='utf-8') as f:
    idx2item = json.load(f)
    # print(idx2item)

test_id = random.choice(user_list)

user_id, item_id = [], []
for _ in range(10):
    user_id.append(test_id)
    item_id.append(random.choice(item_list))

user_id, item_id = np.array(user_id, dtype=np.int32), np.array(item_id, dtype=np.int32)

model = tf.keras.models.load_model('test_model.h5')
preds = model.predict([user_id, item_id])

for u, i, p in zip(user_id, item_id, preds):
    u, i = str(u), str(i)
    print(idx2id[u], idx2item[i], p)

