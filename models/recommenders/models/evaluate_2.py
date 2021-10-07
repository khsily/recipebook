# evaluate.py
import math
import heapq  # for retrieval topK
import numpy as np
from time import time


# from numba import jit, autojit

# Global variables that are shared across processes
_model = None
_user_id = None
_category = None
_K = None


# testNegatives = category, testRatings = user_id
def evaluate_model(model, user_id, category, K, num_thread):
    """
    Evaluate the performance (Hit_Ratio, NDCG) of top-K recommendation
    Return: score of each test rating.
    """
    global _model
    global _user_id
    global _category
    global _K
    _model = model
    _user_id = user_id
    _category = list(category)
    _K = K

    u = _user_id
    items = _category
    # Get prediction scores
    map_item_score = {}
    users = np.full(len(items), u, dtype='int32')
    predictions = _model.predict([users, np.array(items)], batch_size=64, verbose=0)

    for i in range(len(items)):
        item = items[i]
        map_item_score[item] = predictions[i]
    items.pop()

    # Evaluate top rank list
    ranklist = heapq.nlargest(_K, map_item_score, key=map_item_score.get)

    return ranklist



