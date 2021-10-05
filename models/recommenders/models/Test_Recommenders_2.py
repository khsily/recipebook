# Test_Recommenders_2.py
import recommenders.models.ncf as ncf

import sys
import json
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn import model_selection
tf.get_logger().setLevel('ERROR')   # only show error messages

from recommenders.utils.timer import Timer
from recommenders.models.ncf.ncf_singlenode import NCF
from recommenders.models.ncf.dataset import Dataset as NCFDataset
from recommenders.datasets import movielens
from recommenders.utils.notebook_utils import is_jupyter
from recommenders.datasets.python_splitters import python_chrono_split
from recommenders.evaluation.python_evaluation import \
    (rmse, mae, rsquared, exp_var, map_at_k, ndcg_at_k, precision_at_k, recall_at_k, get_top_k_items)

f = open('D:/python/tensorflow2.5/project_ratatouiille/data/index_user.json', 'r', encoding='utf-8')
g = open('D:/python/tensorflow2.5/project_ratatouiille/data/index_item.json', 'r', encoding='utf-8')
index2user = json.load(f)
index2item = json.load(g)
print(index2user)
print(index2item)

f.close()
g.close()

print("System version: {}".format(sys.version))
print("Pandas version: {}".format(pd.__version__))
print("Tensorflow version: {}".format(tf.__version__))

TOP_K = 10

EPOCHS = 50
BATCH_SIZE = 32

SEED = 42

df = pd.read_csv('D:/python/tensorflow2.5/project_ratatouiille/data/test.csv',
                 header=0)

train, test = python_chrono_split(df, 0.75)

data = NCFDataset(train=train, test=test, seed=SEED)


model = NCF(
    n_users=data.n_users,
    n_items=data.n_items,
    model_type='NeuMF',
    n_factors=4,
    layer_sizes=[16, 8, 4],
    n_epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    learning_rate=1e-3,
    verbose=10,
    seed=SEED
)

model.fit(data)

users, items, preds = [], [], []
item = list(train.itemID.unique())
for user in train.userID.unique():
    user = [user] * len(item)
    users.extend(user)
    items.extend(item)
    preds.extend(list(model.predict(user, item, is_list=True)))

    all_predictions = pd.DataFrame(data={'userID': users, 'itemID': items, 'prediction': preds})

    merged = pd.merge(train, all_predictions, on=['userID', 'itemID'], how='outer')
    all_predictions = merged[merged.rating.isnull()].drop('rating', axis=1)

eval_map = map_at_k(test, all_predictions, col_prediction='prediction', k=TOP_K)
eval_ndcg = ndcg_at_k(test, all_predictions, col_prediction='prediction', k=TOP_K)
eval_precision = precision_at_k(test, all_predictions, col_prediction='prediction', k=TOP_K)
eval_recall = recall_at_k(test, all_predictions, col_prediction='prediction', k=TOP_K)

print('MAP: \t %f' % eval_map)
print('NDCG: \t %f' % eval_ndcg)
print('Precision@K: \t %f' % eval_precision)
print('Recall: \t %f' % eval_recall)
user = np.array(all_predictions.userID)
item = np.array(all_predictions.itemID)
preds = np.array(all_predictions.prediction)

for u, i, p in zip(user, item, preds):
    print(index2user[str(u)], index2item[str(i)], p)



