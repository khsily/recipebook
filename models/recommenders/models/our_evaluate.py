# evaluate.py
import math
import random
import numpy as np
import multiprocessing


def evaluate_model(model, K, testPredictions, testLabels, num_thread):
    """
    Evaluate the performance (Hit_Ratio, NDCG) of top-K recommendation
    Return: score of each test rating.
    """

    hits, ndcgs = [], []
    if num_thread > 1:          # Multi-thread
        pool = multiprocessing.Pool(processes=num_thread)
        res = pool.map(predictions, range(len(testLabels)))
        pool.close()
        pool.join()
        hits = [r[0] for r in res]
        ndcgs = [r[1] for r in res]
        return (hits, ndcgs)

    n = 0
    for idx in random.choices(range(len(testLabels)), k=10000):
        print(n)
        (hr, ndcg) = predictions(model, K, testPredictions, testLabels, idx)
        hits.append(hr)
        ndcgs.append(ndcg)
        n += 1

    return (hits, ndcgs)


def predictions(model, K, testPredictions, testLabels, idx):
    pred = testPredictions[idx]
    user_id = [pred[0]] * len(pred[1:])
    item_id = pred[1:]

    user_id, item_id = np.array(user_id, dtype=np.int32), np.array(item_id, dtype=np.int32)

    preds = model.predict([user_id, item_id])

    prediction = []
    for i, p in zip(item_id, preds):
        i, p = str(i), float(p)
        prediction.append([i, p])

    prediction = sorted(prediction, reverse=True, key=lambda x: x[1])

    preds = [int(p[0]) for p in prediction[:K]]

    item = testLabels[idx][1]

    hr = getHitRatio(preds, item)
    ndcg = getNDCG(preds, item)

    return (hr, ndcg)


def getHitRatio(preds, item):
    hr = 0
    for i in preds:
        if i in item:
            hr += 0.1

    return hr


def getNDCG(preds, item):
    dcg, idcg = 0, 0
    for i in range(len(item)):
        idcg += 1 / math.log(i + 2)
        if item[i] in preds:
            dcg += 1 / math.log(i + 2)

    return dcg / idcg
