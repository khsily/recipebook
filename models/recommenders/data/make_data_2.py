# make_data_2.py
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


def get_recommend_title(num):
    '''
    추천 순위 리스트를 받는 함수
    :param num: theme num(list)로 각 테마별 사이트 고유 번호
    :return: theme 별 item title 6개 list
    '''
    url = 'https://wtable.net/api_v2/theme/recipe/list?app_version=1&platform=web&uuid=' \
          '34e239c6-afcd-4fe0-93d4-0ff76a5ad8f7&theme_id={}&order=recommend_desc&offset=0&limit=6'.format(num)
    received = requests.get(url)
    title_recommend_6 = json.loads(received.text)
    # print([i for i in title_200])           # ['success', 'data', 'total_elements']

    title = []
    for i in title_recommend_6['data']:
        title.append(i['title'])

    return title


def make_user_id(unique_theme_title):
    '''
    고유 item의 조합으로 user_id를 만드는 함수
    :param unique_theme_title:
    :return:
    '''
    k = 1
    idx2id = {}
    id2idx = {}
    for i in range(len(unique_theme_title)):
        if i + 1 < len(unique_theme_title):
            for j in unique_theme_title[:i]:
                if len([unique_theme_title[i], unique_theme_title[i + 1], j]) > 2:
                    idx2id[k] = (unique_theme_title[i], unique_theme_title[i + 1], j)
                    id2idx[(unique_theme_title[i], unique_theme_title[i + 1], j)] = k
                    k += 1

    for i in range(len(unique_theme_title)):
        if i + 2 < len(unique_theme_title):
            for j in unique_theme_title[:i]:
                if len([unique_theme_title[i], unique_theme_title[i + 1], unique_theme_title[i + 2], j]) > 3:
                    idx2id[k] = (unique_theme_title[i], unique_theme_title[i + 1],
                                 unique_theme_title[i + 2], j)
                    id2idx[(unique_theme_title[i], unique_theme_title[i + 1],
                            unique_theme_title[i + 2], j)] = k
                    k += 1

    for i in range(len(unique_theme_title)):
        if i + 3 < len(unique_theme_title):
            for j in unique_theme_title[:i]:
                if len([unique_theme_title[i], unique_theme_title[i + 1],
                        unique_theme_title[i + 2], unique_theme_title[i + 3], j]) > 4:
                    idx2id[k] = (unique_theme_title[i], unique_theme_title[i + 1],
                                 unique_theme_title[i + 2], unique_theme_title[i + 3], j)
                    id2idx[(unique_theme_title[i], unique_theme_title[i + 1],
                            unique_theme_title[i + 2], unique_theme_title[i + 3], j)] = k
                    k += 1

    return idx2id, id2idx


def item_theme(category_name):
    '''
    테마별 요리 음식이 들어간 딕셔너리와 요리이름 리스트를 반환한다.
    :param category_name: category의 이름 리스트
    :return: 테마: 아이템 딕셔너리, 요리 이름 리스트
    '''
    with open('recipc_list_utf_8.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    item_title, name = {}, []
    for d in data['list']:
        if d['catagory_name'] == category_name:
            name.append(d['title'])
            item_title[d['catagory_name']] = name

    return item_title, name


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

    f = open(path, 'w', encoding='utf-8')

    for i in idx2id:
        for_unique = []
        for j in idx2id[i]:
            print('{}\t{}\t{}'.format(i, item2idx[j], random.choice(rating)), file=f)
            for_unique.append(j)
            for _ in range(5):
                for t in range(7):
                    if j in list(theme2item.values())[t]:
                        name = random.choice(list(theme2item.values())[t])
                        if j != name and name not in for_unique:
                            print('{}\t{}\t{}'.format(i, item2idx[name], random.choice(rating)), file=f)
                            for_unique.append(name)

    f.close()


def test_rating(path, idx2id, idx2item, rating):
    '''
    각 아이디마다 평가하지 않았던 항목 한개에 대해 평가.
    :param path: save path
    :param idx2id: dict {0: (요리명, 요리명), ...}
    :param idx2item: dict {0: 요리명, 1: 요리명, ...}
    :param rating: 평가 점수 리스트
    :return: None path에 파일로 저장
    '''
    df = pd.read_csv('recipe.train.rating', delimiter='\t', names=['user_id', 'item_id', 'rating'])
    f = open(path, 'w', encoding='utf-8')
    test_item = []
    while len(test_item) <= max(df['user_id']):
        for i in idx2id:
            print(i)
            # food_name = random.choice()
            rated = df.loc[df['user_id'] == i].item_id.values
            new = random.choice(list(idx2item.keys()))
            if new not in rated and len(test_item) < max(df['user_id']):
                test_item.append(new)
        if len(test_item) == max(df['user_id']):
            break

    for i, n in zip(idx2id, test_item):
        print('{}\t{}\t{}'.format(i, n, random.choice(rating)), file=f)

    f.close()


def test_negative(path, item2idx):
    '''
    (user_id, rated item_id) unrated item_id, ...
    :param path: save file path
    :param item2idx: dict {요리명: 0, ...}
    :return: None recipe.test.negative 파일 생성
    '''
    df = pd.read_csv('recipe.train.rating', delimiter='\t', names=['user_id', 'item_id', 'rating'])
    pos_rat = []
    for i in range(1, max(df['user_id'])+1):
        rated = df.loc[df['user_id'] == i].item_id.values
        pos_rat.append([str(r) for r in rated])
    # print(len(pos_rat))                 # 2341

    g = open(path, 'w', encoding='utf-8')
    # f = open('ml-1m.test.negative', 'r', encoding='utf-8')
    # sample = f.readline()
    # print(sample)
    # print(type(sample.split('\t')[1]))

    with open('recipe.test.rating', 'r', encoding='utf-8') as f:
        rows = f.readlines()
        id_rat, pos_list = [], []
        for row in rows:
            # print(row.split()[0], row.split()[1])
            id = '({},{})'.format(int(row.split()[0]), int(row.split()[1]))
            id_rat.append(id)
            pos_rat[int(row.split()[0])-1].append(row.split()[1])
            rated = pos_rat[int(row.split()[0])-1]
            pos_list.append(rated)
        # print(len(pos_list))            # 2341

        neg_list, li = [], []
        for l in pos_list:
            while len(li) < 99:
                neg = item2idx[random.choice(list(item2idx.keys()))]
                if neg not in l and neg not in neg_list:
                    li.append(neg)
            neg_list.append(li)
            li = []

        # print(len(neg_list))                    # 2341
        # print(len(neg_list[0]))                 # 99

        for i, n in zip(id_rat, neg_list):
            print(i, *n, file=g)

    g.close()


def make_json(path, file):
    if os.path.exists(path):
        print('pass')
        pass
    else:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(file, f)


def test():
    food_name = [
        '짜장면', '탕수육', '짬뽕', '유린기', '볶음밥', '깐쇼새우', '떡볶이', '오뎅탕', '김치볶음밥', '김밥',
        '라면', '우동', '잔치국수', '후라이드치킨', '피자', '양념치킨', '토마토 파스타', '까르보나라', '알리오올리오', '봉골레 파스타',
        '크림 파스타', '크림 리조또', '토마토 리조또', '치킨 샐러드', '샌드위치', '리코타 치즈 샐러드', '발사믹 토마토 샐러드', '단호박 샐러드', '닭가슴살 샐러드', '양배추 샐러드'
    ]

    food_name_idx = {n: i for i, n in enumerate(food_name, 1)}

    theme = {'chinese': ['짜장면', '탕수육', '짬뽕', '유린기', '볶음밥', '깐쇼새우'],
             'boonsik': ['떡볶이', '오뎅탕', '김치볶음밥', '김밥', '라면', '우동', '잔치국수'],
             'high_kcal': ['후라이드치킨', '피자', '양념치킨'],
             'western': ['토마토 파스타', '까르보나라', '알리오올리오', '봉골레 파스타',
                         '크림 파스타', '크림 리조또', '토마토 리조또'],
             'diet': ['치킨 샐러드', '샌드위치', '리코타 치즈 샐러드', '발사믹 토마토 샐러드',
                      '단호박 샐러드', '닭가슴살 샐러드', '양배추 샐러드']}

    chinese = [1, 2, 3, 4, 5, 6]
    boonsik = [7, 8, 9, 10, 11, 12, 13]
    high_kcal = [14, 15, 16]
    western = [17, 18, 19, 20, 21, 22, 23]
    diet = [24, 25, 26, 27, 28, 29, 30]

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

    # pprint.pprint(id)

    # print(len(id))              # 169
    # print(len(food_name))       # 30

    # zero_act = np.zeros([169, 30], dtype=np.int32)
    # print(zero_act.shape)
    # print(zero_act)

    # f = open('test.csv', 'w', encoding='utf-8')
    # df = pd.DataFrame(zero_act, index=id.keys(), columns=food_name)
    # print(tabulate(df, headers=food_name, tablefmt='psql'), file=f)
    # print(df, file=f)
    # f.close()
    # g = open('D:/python/tensorflow2.5/project_ratatouiille/data/index_user.json', 'w', encoding='utf-8')
    # json.dump(id, g)
    # i = open('D:/python/tensorflow2.5/project_ratatouiille/data/index_item.json', 'w', encoding='utf-8')
    # json.dump(food_name_idx, i)

    # g.close()
    # i.close()

    def make_data():
        rating = [i for i in np.linspace(1, 10, 10, dtype=np.int32)]

        # id_idx = id.keys()
        # id_idx = list(id_idx)
        f = open('test.train.rating', 'w', encoding='utf-8')

        for i in id:
            for_unique = []
            for j in id[i]:
                print('{}\t{}\t{}'.format(i, food_name_idx[j], random.choice(rating)), file=f)
                for_unique.append(j)
                for _ in range(5):
                    for t in range(5):
                        if j in list(theme.values())[t]:
                            name = random.choice(list(theme.values())[t])
                            if j != name and name not in for_unique:
                                print('{}\t{}\t{}'.format(i, food_name_idx[name], random.choice(rating)), file=f)
                                for_unique.append(name)

        f.close()

    # make_data()
    with open('test.test', 'w', encoding='utf-8') as f:
        for i in list(theme.values()):
            for j in i:
                print('{}|{}'.format(1, food_name_idx[j]), file=f)


# test()

theme_num = [185, 186, 187, 188, 189, 190, 193]
category_name = ['한식', '양식', '일식', '중식', '퓨전', '분식', '다이어트']

theme_title_top6 = []
for n in theme_num:
    theme_title_top6 += get_recommend_title(n)

# with open('theme_title.csv', 'w', encoding='utf-8') as f:
#     wr = csv.writer(f)
#     wr.writerow([t for t in theme_title_top6])

unique_top6 = list(collections.Counter(theme_title_top6).keys())

idx2id, id2idx = make_user_id(unique_top6)


theme2item, title = {}, []
for name in category_name:
    theme2item.update(item_theme(name)[0])
    title += item_theme(name)[1]

title = set(title)

item2idx = {n: i for i, n in enumerate(title)}
idx2item = {i: n for i, n in enumerate(title)}

# print(len(unique_top6))             # 42
# print(len(title))                   # 827

# id 선택 메뉴에 대해 평가
rating = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# train_rating('recipe.train.rating', idx2id, item2idx, theme2item, rating)     # 파일 만듬
# test_rating('recipe.test.rating', idx2id, idx2item, rating)                   # 파일 만듬
# test_negative('recipe.test.negative', item2idx)                               # 파일 만듬

# print(id2idx)

# make_json('idx2id.json', idx2id)
# make_json('idx2item.json', idx2item)

with open('item_idx.csv', 'w', encoding='utf-8') as f:
    print([i for i in list(idx2item.keys())], file=f)

with open('id_idx.csv', 'w', encoding='utf-8') as f:
    print([i for i in list(idx2id.keys())], file=f)






