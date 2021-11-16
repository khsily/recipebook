# make_data.py
import requests
import json
import pprint
import collections
import random
import pandas as pd
import numpy as np
import os
import re
import csv


def get_recommend_title():
    '''
    추천 순위 리스트를 받는 함수
    :param num: theme num(list)로 각 테마별 사이트 고유 번호
    :return: theme 별 item title 6개 list
    '''
    top6 = pd.read_csv('top6_1.csv', delimiter=',', header=None)
    top6 = top6.dropna(axis=1)
    pd.DataFrame(top6).columns = ['category', 'title']
    top6_title = list(top6.title)

    return top6_title


def get_user_id(path):
    f = open(path, 'r', encoding='utf-8')
    idx2id, id2idx = {}, {}
    for row in f.readlines():
        row = row.split('|')
        row[1] = row[1].strip()
        row[1] = tuple(re.sub('[\(\)\']', '', row[1]).split(','))
        idx2id[row[0]] = row[1]
        id2idx[row[1]] = row[0]

    return idx2id, id2idx


def train_rating(path, idx2id, item2idx, theme2item, rating):
    '''
    user_id     item_id     rating
    int         int         int
    :param path: save path
    :param idx2id: dict {0: (요리명, 요리명), ...}
    :param item2idx: dict {요리명: 0, ...}
    :param theme2item: dict {한식: [요리명, 요리명, ...}
    :param rating: 평가 점수 리스트
    :return: None path에 파일로 저장
    '''

    f = open(path, 'a', encoding='utf-8')
    often_use, num = {}, 0
    for i in idx2id:
        print(num)
        for_unique = []
        for j in idx2id[i]:
            j = j.strip()
            print('{}\t{}\t{}'.format(i, item2idx[j], 5), file=f)
            often_use[i] = [item2idx[j]]
            for_unique.append(j)
            for _ in range(30):
                for t in range(7):
                    if j in list(theme2item.values())[t]:
                        name = random.choice(list(theme2item.values())[t])
                        if j != name and name not in for_unique:
                            print('{}\t{}\t{}'.format(i, item2idx[name], random.choice(rating)), file=f)
                            often_use[i].append(item2idx[name])
                            for_unique.append(name)
        num += 1
    f.close()

    return often_use


def test_rating(path, idx2item, rating):
    '''
    각 아이디마다 평가하지 않았던 항목 한개에 대해 평가.
    :param path: save path
    :param idx2item: dict {0: 요리명, 1: 요리명, ...}
    :param rating: 평가 점수 리스트
    :return: None path에 파일로 저장
    '''
    user_id, used_item = [], []
    with open('once_recipe.test.label', 'r', encoding='utf-8') as f:
        for row in f.readlines():
            user_id.append(row.strip().split(',')[0])
            used_item.append(row.strip().split(',')[1:])

    f = open(path, 'w', encoding='utf-8')
    test_item = []
    while len(test_item) <= 123410:
        for u, i in zip(user_id, used_item):
            print(u)
            # food_name = random.choice()
            rated = i
            new = random.choice(list(idx2item.keys()))
            if new not in rated and len(test_item) <= 123410:
                test_item.append(new)
        if len(test_item) == 123410:
            break

    for i, n in zip(user_id, test_item):
        print('{}\t{}\t{}'.format(i, n, random.choice(rating)), file=f)

    f.close()


def test_negative(path, item2idx):
    '''
    (user_id, rated item_id) unrated item_id, ...
    :param path: save file path
    :param item2idx: dict {요리명: 0, ...}
    :return: None recipe.test.negative 파일 생성
    '''
    user_id, used_item = [], []
    with open('once_recipe.test.label', 'r', encoding='utf-8') as f:
        for row in f.readlines():
            user_id.append(row.strip().split(',')[0])
            used_item.append(row.strip().split(',')[1:])

    g = open(path, 'w', encoding='utf-8')
    with open('once_recipe.test.rating', 'r', encoding='utf-8') as f:
        id_rat, item, pos_list = [], [], []
        for row in f.readlines():
            id = '({},{})'.format(int(row.split()[0]), int(row.split()[1]))
            id_rat.append(id)
            item.append(row.split()[1])

        for items, i in zip(used_item, item):
            items.append(str(i))
            pos_list.append(items)

        neg_list, li = [], []
        for l in pos_list:
            while len(li) < 99:
                neg = item2idx[random.choice(list(item2idx.keys()))]
                if neg not in l:
                    li.append(neg)
            neg_list.append(li)
            li = []

        # print(len(neg_list))                    # 2341
        # print(len(neg_list[0]))                 # 99

        for i, n in zip(id_rat, neg_list):
            print(i, *n, file=g)

    g.close()


def make_user_pick(item2idx):
    df = pd.read_csv('user_like_act.csv', delimiter='|', header=None,
                     names=['user_idx', 'user_id', 'item_name', 'rating'])
    df = df.dropna()
    with open('recipe.train.rating', 'a', encoding='utf-8') as f:
        for idx, item, rating in zip(df.user_idx, df.item_name, df.rating):
            print('{}\t{}\t{}'.format(idx, item2idx[item], int(rating)), file=f)


theme_num = [185, 186, 187, 188, 189, 190, 193]
category_name = ['pad', '한식', '중식', '양식', '일식', '퓨전', '분식', '다이어트']
rating = [1, 2, 3, 4, 5]

theme_title_top6 = get_recommend_title()

idx2id, id2idx = get_user_id('idx_id.csv')

item_title = pd.read_csv('csv_final/csv_final/recipe.csv', delimiter=',')

theme2item, title = {}, []
for C in category_name:
    for c, t in zip(item_title.category_id.values, item_title.title.values):
        if C == category_name[c]:
            title.append(t.strip())
    theme2item[C] = title
    title = []

del(theme2item['pad'])

i_title = [i.strip() for i in list(item_title.title.values)]

item2idx = {n: i for i, n in zip(list(item_title.id.values), i_title)}
idx2item = {i: n for i, n in zip(list(item_title.id.values), i_title)}

# print(len(theme2item))              # 7
# for i in theme2item:                # 한식 328, 중식 75, 양식 225, 일식 58, 퓨전 78, 분식 48, 다이어트 79
#     print(len(theme2item[i]))
# print(len(i_title))                   # 891

# make_user_pick(item2idx)
for_record = {}
for i in idx2id:
    for_record[i] = []

often_use = train_rating('once_recipe.train.rating', idx2id, item2idx, theme2item, rating)     # 파일 만듬
for j in often_use:
    for_record[j] += (often_use[j])

with open('once_recipe.test.label', 'w', encoding='utf-8') as f:
    for i in for_record:
        print(i, *[j[0] for j in collections.Counter(for_record[i]).most_common()], sep=',', file=f)

test_rating('once_recipe.test.rating', idx2item, rating)                   # 파일 만듬
test_negative('once_recipe.test.negative', item2idx)                               # 파일 만듬
