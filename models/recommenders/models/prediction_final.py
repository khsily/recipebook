# prediction_final.py
import tensorflow as tf
import numpy as np


def predictions(user_id, item_id, model_path):
    user_id = user_id * len(item_id)

    user_id, item_id = np.array(user_id, dtype=np.int32), np.array(item_id, dtype=np.int32)

    model = tf.keras.models.load_model(model_path)
    preds = model.predict([user_id, item_id])

    predictions = []
    for i, p in zip(item_id, preds):
        i, p = str(i), float(p)
        predictions.append([i, p])

    predictions = sorted(predictions, reverse=True, key=lambda x: x[1])
    recommends = [p[0] for p in predictions[:10]]

    return recommends


if __name__ == '__main__':
    model_path = 'D:\python\\tensorflow2.5\\recipebook\models\\recommenders\models\\test_model.h5'

    user_id = [3]
    item_id = [2, 6, 199, 235]          # 카테고리에 속한 요리 갯수 만큼 중복되지 않게 들어와야 함.

    recommends_top10 = predictions(user_id, item_id, model_path)

    print(recommends_top10)



