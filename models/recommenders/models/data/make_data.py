# make_data.py
import re
import random
import pandas as pd


def make_id_combination(path):
    '''
    :param path: recipe data file path
    :return: none save idx_idx to csv
    '''
    f = open('idx_id.csv', 'w', encoding='utf-8')
    df = pd.read_csv(path, names=['id', 'recipe_id', 'category', 'recipe_name'])
    df = df.dropna()
    recipe_id = df.recipe_name.values
    combi, i = [], 0
    for idx in range(len(recipe_id)):
        for idx_2 in range(len(recipe_id) + 1):
            for idx_3 in range(len(recipe_id) + 2):
                if len(recipe_id) > idx_2 and len(recipe_id) > idx_3 and idx != idx_2 \
                        and idx != idx_3 and idx_2 != idx_3:
                    if sorted((idx, idx_2, idx_3)) not in combi:
                        i += 1
                        combi.append(sorted((idx, idx_2, idx_3)))
                        print(i, '|', (recipe_id[idx], recipe_id[idx_2], recipe_id[idx_3]), file=f)
                        for idx_4 in range(len(recipe_id)):
                            if idx != idx_4 and idx_2 != idx_4 and idx_3 != idx_4 and \
                                    sorted((idx, idx_2, idx_3, idx_4)) not in combi:
                                combi.append(sorted((idx, idx_2,
                                                     idx_3, idx_4)))
                                i += 1
                                print(i, '|', (recipe_id[idx], recipe_id[idx_2],
                                               recipe_id[idx_3], recipe_id[idx_4]), file=f)
                                print(i)

    f.close()


def get_user_id(path):
    '''
    :param path: idx_id path
    :return: idx2id: dict {0: (요리명, 요리명), ...}, id2idx: {(요리명, 요리명): 0, ...}
    '''
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
    :return: often_use: dict {id: [요리idx, ...]}
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
            for _ in range(10):
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
    with open('10_recipe.test.label', 'r', encoding='utf-8') as f:
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
    with open('10_recipe.test.label', 'r', encoding='utf-8') as f:
        for row in f.readlines():
            user_id.append(row.strip().split(',')[0])
            used_item.append(row.strip().split(',')[1:])

    g = open(path, 'w', encoding='utf-8')
    with open('10_recipe.test.rating', 'r', encoding='utf-8') as f:
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


# 사용한 데이터의 카테고리를 미리 선정함.
category_name = ['pad', '한식', '중식', '양식', '일식', '퓨전', '분식', '다이어트']
rating = [1, 2, 3, 4, 5]

# 아이디 조합 csv 파일로 생성 및 저장
# make_id_combination('csv_final/csv_final/favor_full.csv')

# 아이디 조합에 대해 인덱스와 아이디 조합 딕셔너리 변수 저장
idx2id, id2idx = get_user_id('idx_id.csv')

# 레시피 데이터 변수에 저장
item_title = pd.read_csv('csv_final/csv_final/recipe.csv', delimiter=',')

# 테마와 레시피 타이틀 딕셔너리
theme2item, title = {}, []
for C in category_name:
    for c, t in zip(item_title.category_id.values, item_title.title.values):
        if C == category_name[c]:
            title.append(t.strip())
    theme2item[C] = title
    title = []

del(theme2item['pad'])

# 레시피 타이틀과 인덱스 조합 딕셔너리 변수 저장
i_title = [i.strip() for i in list(item_title.title.values)]
item2idx = {n: i for i, n in zip(list(item_title.id.values), i_title)}
idx2item = {i: n for i, n in zip(list(item_title.id.values), i_title)}

# 테마와 테마별 아이템 갯수, 전체 아이템 갯수 확인.
# print(len(theme2item))              # 7
# for i in theme2item:                # 한식 328, 중식 75, 양식 225, 일식 58, 퓨전 78, 분식 48, 다이어트 79
#     print(len(theme2item[i]))
# print(len(i_title))                   # 891


# 트레인 데이터 생성
# often_use = train_rating('10_recipe.train.rating', idx2id, item2idx, theme2item, rating)
# for j in often_use:
#     for_record[j] += (often_use[j])

# 테스트 라벨 데이터 생성
# with open('10_recipe.test.label', 'w', encoding='utf-8') as f:
#     for i in for_record:
#         print(i, *[j[0] for j in collections.Counter(for_record[i]).most_common()], sep=',', file=f)

# 모델 테스트를 위한 데이터 생성
# test_rating: 정답 데이터 생성
# test_rating('10_recipe.test.rating', idx2item, rating)
# test_negative: 평가하지 않은 데이터 생성
# test_negative('10_recipe.test.negative', item2idx)
