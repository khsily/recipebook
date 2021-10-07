# make_data.py
import csv
import json
import pandas as pd
import pprint
import numpy as np
import random
import collections


'''
데이터 포맷
train.rating
user_id     ::      movie_id        ::      rating  ::      timestamp    한 유저가 최소 20개 이상의 영화를 평가함
(음식 조합)         (평가 음식)             (평가)


test.rating
user_id::movie_id::rating::timestamp    각 유저 한번씩 새로운 영화에 대해 평가함

test.negative                           각 유저가 한번도 보지 않은 영화 99개
(user_id, movie_id)::movie_id1::movie_id2::...

'''

pd.set_option('max_columns', 1000)
pd.set_option('max_rows', 1000)
pd.set_option('display.width', 1000)


def test():
    food_name = [
        '짜장면', '탕수육', '짬뽕', '유린기', '볶음밥', '깐쇼새우', '떡볶이', '오뎅탕', '김치볶음밥', '김밥',
        '라면', '우동', '잔치국수', '후라이드치킨', '피자', '양념치킨', '토마토 파스타', '까르보나라', '알리오올리오', '봉골레 파스타',
        '크림 파스타', '크림 리조또', '토마토 리조또', '치킨 샐러드', '샌드위치', '리코타 치즈 샐러드', '발사믹 토마토 샐러드', '단호박 샐러드', '닭가슴살 샐러드', '양배추 샐러드'
    ]

    food_name_idx = {i: n for i, n in enumerate(food_name, 1)}

    chinese = [1, 2, 3, 4, 5, 6]
    boonsik = [7, 8, 9, 10, 11, 12, 13]
    high_kcal = [14, 15, 16]
    western = [17, 18, 19, 20, 21, 22, 23]
    diet = [24, 25, 26, 27, 28, 29, 30]


    id_name_food = ['짜장면', '탕수육', '짬뽕', '라면', '김밥',
                    '우동', '토마토 파스타', '크림 파스타', '후라이드 치킨', '피자',
                    '크림 리조또', '치킨 샐러드', '샌드위치', '닭가슴살 샐러드']
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
                if len([id_name_food[i], id_name_food[i+1], j]) > 2:
                    id[k] = (id_name_food[i], id_name_food[i+1], j)
                    k += 1

    pprint.pprint(id)
    exit()
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
    g = open('D:/python/tensorflow2.5/project_ratatouiille/data/index_user.json', 'w', encoding='utf-8')
    json.dump(id, g)
    i = open('D:/python/tensorflow2.5/project_ratatouiille/data/index_item.json', 'w', encoding='utf-8')
    json.dump(food_name_idx, i)

    g.close()
    i.close()

    def make_data(cwr, category, start, end):
        rating = [i for i in np.linspace(0, 5, 11)]

        id_idx = id.keys()
        id_idx = list(id_idx)

        for i in id_idx[start:end]:
            cwr.writerow([str(i), random.choice(category), random.choice(rating)])


    # f = open('test.csv', 'a', encoding='utf-8')
    # cwr = csv.writer(f)
    # cwr.writerow(['userID', 'itemID', 'rating', 'timestamp'])

    # make_data(cwr, chinese, 0, 15)
    # make_data(cwr, boonsik, 0, 15)
    # make_data(cwr, high_kcal, 0, 15)
    # make_data(cwr, western, 16, 29)
    # make_data(cwr, boonsik, 16, 29)
    # make_data(cwr, chinese, 16, 29)
    # make_data(cwr, high_kcal, 29, 46)
    # make_data(cwr, chinese, 29, 46)
    # make_data(cwr, western, 29, 46)
    # make_data(cwr, diet, 46, 78)
    # make_data(cwr, high_kcal, 46, 78)
    # make_data(cwr, diet, 46, 78)
    # make_data(cwr, chinese, 46, 78)
    # make_data(cwr, boonsik, 46, 78)
    # make_data(cwr, diet, 46, 78)
    # make_data(cwr, diet, 78, 91)
    # make_data(cwr, diet, 78, 91)
    # make_data(cwr, diet, 78, 91)
    # make_data(cwr, western, 78, 91)
    # make_data(cwr, chinese, 78, 91)
    # make_data(cwr, boonsik, 78, 91)
    # make_data(cwr, chinese, 92, 102)
    # make_data(cwr, chinese, 92, 102)
    # make_data(cwr, boonsik, 92, 102)
    # make_data(cwr, boonsik, 92, 102)
    # make_data(cwr, western, 102, 120)
    # make_data(cwr, western, 102, 120)
    # make_data(cwr, chinese, 102, 120)
    # make_data(cwr, boonsik, 102, 120)
    # make_data(cwr, high_kcal, 102, 120)
    # make_data(cwr, high_kcal, 120, 137)
    # make_data(cwr, high_kcal, 120, 137)
    # make_data(cwr, high_kcal, 120, 137)
    # make_data(cwr, western, 120, 137)
    # make_data(cwr, chinese, 120, 137)
    # make_data(cwr, diet, 137, 170)
    # make_data(cwr, diet, 137, 170)
    # make_data(cwr, diet, 137, 170)
    # make_data(cwr, western, 137, 170)
    # make_data(cwr, boonsik, 137, 170)
    #
    # f.close()
    #
    # print(data)


# test()

'''
아이디 만든 방법 -> 카테고리 별로 대표할 만한 음식을 고름 x 그냥 유니크 요리명에서 조합 만들기-> 2개 3개 4개 5개 선택한 선택지를 만듬
-> 번호를 붙여 아이디로 사용.
'''


with open('recipc_list_utf_8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def title_dictionary_catagory(catagory):
    dic_title = {catagory: [d['title'] for d in data['list'] if d['catagory_name'] == catagory]}
    return dic_title


title, dic_tit = [], {}
for d in data['list']:
    title.append(d['title'])
    dic_tit.update(title_dictionary_catagory(d['catagory_name']))

unique_title = list(collections.Counter(title).keys())
pprint.pprint(unique_title)

# k = 1
# id = {}
# for i in range(len(unique_title)):
#     pair = [(unique_title[i], j) for j in unique_title[:i] if j != unique_title[i]]
#     for idx1, idx2 in pair:
#         id[k] = (idx1, idx2)
#         k += 1
#
# for i in range(len(unique_title)):
#     if i + 1 < len(unique_title):
#         for j in unique_title[:i]:
#             if len([unique_title[i], unique_title[i + 1], j]) > 2:
#                 id[k] = (unique_title[i], unique_title[i + 1], j)
#                 k += 1
#





