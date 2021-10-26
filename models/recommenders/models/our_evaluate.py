# evaluate.py
import math
import numpy as np
import tensorflow as tf

# Global variables that are shared across processes
_model, _K = None, None
_testPredictions = None
_testLabels = None


def evaluate_model(model, K, testPredictions, testLabels):
    """
    Evaluate the performance (Hit_Ratio, NDCG) of top-K recommendation
    Return: score of each test rating.
    """
    global _model
    global _K
    global _testPredictions
    global _testLabels
    _model, _K = model, K
    _testPredictions = testPredictions
    _testLabels = testLabels

    hits, ndcgs = [], []
    for idx in range(len(_testPredictions)):
        preds = predictions(idx)
        item = get_label(idx)
        hr = getHitRatio(preds, item)
        ndcg = getNDCG(preds, item)
        hits.append(hr)
        ndcgs.append(ndcg)

    return (hits, ndcgs)


def predictions(idx):
    pred = _testPredictions[idx]
    user_id = [pred[0]] * len(pred[1:])
    item_id = pred[1:]

    user_id, item_id = np.array(user_id, dtype=np.int32), np.array(item_id, dtype=np.int32)

    preds = _model.predict([user_id, item_id])

    predictions = []
    for i, p in zip(item_id, preds):
        i, p = str(i), float(p)
        predictions.append([i, p])

    predictions = sorted(predictions, reverse=True, key=lambda x: x[1])

    return [int(p[0]) for p in predictions[:_K]]


def get_label(idx):
    labels = _testLabels[idx][1:]
    labels = labels[0]
    return labels


def getHitRatio(preds, item):
    hr = 0
    for i in preds:
        if i in item:
            hr += 1

    return hr


def getNDCG(preds, item):
    dcg, idcg = 0, 0
    for i in range(len(item)):
        idcg += 1 / math.log(i + 2)
        if item[i] in preds:
            dcg += 1 / math.log(i + 2)

    return dcg / idcg
