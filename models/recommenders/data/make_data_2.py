# make_data_2.py
import requests
import json
import pprint
import collections
import random
import pandas as pd
import os


def get_recommend_title(num):
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
    with open('recipc_list_utf_8.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    item_title, name, title = {}, [], []
    for d in data['list']:
        title.append(d['title'])
        if d['catagory_name'] == category_name:
            name.append(d['title'])
            item_title[d['catagory_name']] = name

    idx2item = {int(i): n for i, n in enumerate(list(collections.Counter(title).keys()))}
    item2idx = {n: int(i) for i, n in enumerate(list(collections.Counter(title).keys()))}

    return item_title, idx2item, item2idx


def train_rating():
    # id 선택 메뉴에 대해 평가
    rating = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    f = open('recipe.train.rating', 'a', encoding='utf-8')
    print('{}\t{}\t{}'.format('user_id', 'item_id', 'rating'), file=f)

    for i in idx2id:
        for_unique = []
        for j in idx2id[i]:
            print('{}\t{}\t{}'.format(i, item2idx[j], random.choice(rating)), file=f)
            for_unique.append(j)
            for _ in range(5):
                for t in range(11):
                    if j in list(theme2item.values())[t]:
                        name = random.choice(list(theme2item.values())[t])
                        if j != name and name not in for_unique:
                            print('{}\t{}\t{}'.format(i, item2idx[name], random.choice(rating)), file=f)
                            for_unique.append(name)

    f.close()


def make_json(path, file):
    if os.path.exists(path):
        print('pass')
        pass
    else:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(file, f)


# def test_rating():
#     # id 선택 메뉴에 대해 평가
#     rating = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
#     df = pd.read_csv('recipe.train.rating', delimiter='\t', header=0)
#     for i in idx2id:
#         food_name = random.choice()
#         print(df.loc[df.user_id == i].item_id.values)
#
#     exit()
#
#     # print('{}\t{}\t{}'.format('user_id', 'item_id', 'rating'), file=f)
#
#     for i in idx2id:
#         for_unique = []
#         for j in idx2id[i]:
#             print('{}\t{}\t{}'.format(i, item2idx[j], random.choice(rating)), file=f)
#             for_unique.append(j)
#             for _ in range(5):
#                 for t in range(11):
#                     if j in list(theme2item.values())[t]:
#                         name = random.choice(list(theme2item.values())[t])
#                         if j != name and name not in for_unique:
#                             print('{}\t{}\t{}'.format(i, item2idx[name], random.choice(rating)), file=f)
#                             for_unique.append(name)

theme_num = [1, 183, 5, 126, 2, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 214, 242]
category_name = ['메인요리', '밑반찬', '간식', '간단요리', '초대요리', '채식',
                 '한식', '양식', '일식', '중식', '퓨전', '분식', '안주', '베이킹',
                 '다이어트', '도시락', '키토']

theme_title_top6 = []
for n in theme_num:
    theme_title_top6 += get_recommend_title(n)

unique_top6 = list(collections.Counter(theme_title_top6).keys())

idx2id, id2idx = make_user_id(unique_top6)

theme2item = {}
for name in category_name:
    theme2item.update(item_theme(name)[0])


_, idx2item, item2idx = item_theme(category_name)

# train_rating()

# make_json('idx2id.json', idx2id)
make_json('idx2item.json', idx2item)

# test_rating()