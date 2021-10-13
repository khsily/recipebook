# prediction.py
import tensorflow as tf
import numpy as np
import pandas as pd
import random
import pprint
import re


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
            if t == c:
                item_list.append(i)
        theme_item[c] = item_list
        item_list = []

    return theme_item


def predictions(test_id, choose_category):
    user_id, item_id = [], []
    for i in choose_category:
        for j in theme_item[i]:
            user_id.append(test_id)
            item_id.append(item2idx[j])

    item_id = list(set(item_id))
    user_id = user_id[:len(item_id)]

    user_id, item_id = np.array(user_id, dtype=np.int32), np.array(item_id, dtype=np.int32)

    model = tf.keras.models.load_model('test_model.h5')
    preds = model.predict([user_id, item_id])

    predictions = []
    for u, i, p in zip(user_id, item_id, preds):
        u, i, p = str(u), str(i), float(p)
        predictions.append([idx2id[u], idx2item[i], p])

    predictions = sorted(predictions, reverse=True, key=lambda x: x[2])
    recommends = [p[1] for p in predictions[:10]]

    return recommends


if __name__ == '__main__':
    user_idx, user_list = get_data('data\idx_id.csv')
    item_idx, item_list = get_data('data\idx_item.csv')
    theme, item = get_data('data\\theme_item.csv')

    idx2id, id2idx = make_idx2_st(user_idx, user_list)
    idx2item, item2idx = make_idx2_st(item_idx, item_list)

    category_name = ['한식', '양식', '일식', '중식', '퓨전', '분식', '다이어트']

    theme_item = theme_dic(category_name, theme, item)

    random.seed(100)
    test_id = random.choice(user_idx)                   # input user_idx
    choose_category = ['한식', '분식', '다이어트']       # input category

    recommends_top10 = predictions(test_id, choose_category)

    print(recommends_top10)

