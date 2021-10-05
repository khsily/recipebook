# GMF.py
import numpy as np
import tensorflow as tf
import pandas as pd
from dataset_2 import Dataset as Dataset
from dataset import Dataset as Dataset_2

from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.models import Sequential, Model, load_model, save_model
from tensorflow.keras.layers import Dense, Lambda, Activation
from tensorflow.keras.layers import Embedding, Input, Dense, Add, Reshape, Concatenate, Flatten
from tensorflow.keras.optimizers import Adagrad, Adam, SGD, RMSprop
from tensorflow.keras.regularizers import l2
from time import time
from evaluate import evaluate_model
from sklearn import model_selection
import multiprocessing as mp
import sys
import math
import argparse


def get_model(num_users, num_items, latent_dim):
    # Input variables
    user_input = Input(shape=(1,), dtype='int32', name='user_input')
    item_input = Input(shape=(1,), dtype='int32', name='item_input')

    MF_Embedding_User = Embedding(input_dim=num_users, output_dim=latent_dim, name='user_embedding',
                                  embeddings_initializer=glorot_uniform, embeddings_regularizer='l2', input_length=1)
    MF_Embedding_Item = Embedding(input_dim=num_items, output_dim=latent_dim, name='item_embedding',
                                  embeddings_initializer=glorot_uniform, embeddings_regularizer='l2', input_length=1)

    # Crucial to flatten an embedding vector!
    user_latent = Flatten()(MF_Embedding_User(user_input))
    item_latent = Flatten()(MF_Embedding_Item(item_input))

    # Element-wise product of user and item embeddings
    predict_vector = tf.keras.layers.multiply([user_latent, item_latent])

    # Final prediction layer
    # prediction = Lambda(lambda x: K.sigmoid(K.sum(x)), output_shape=(1,))(predict_vector)
    prediction = Dense(1, activation='sigmoid', name='prediction')(predict_vector)

    model = Model([user_input, item_input], prediction)

    model.summary()

    return model


def get_train_instances(train, num_negatives):
    user_input, item_input, labels = [], [], []
    num_users = train.shape[0]

    for (u, i) in train.keys():
        # positive instance
        user_input.append(u)
        item_input.append(i)
        labels.append(1)
        # negative instances
        for t in range(num_negatives):
            j = np.random.randint(num_items)
            while train.has_key((u, j)):
                j = np.random.randint(num_items)
            user_input.append(u)
            item_input.append(j)
            labels.append(0)
    return user_input, item_input, labels


df = pd.read_csv('D:/python/tensorflow2.5/project_ratatouiille/data/test.csv',
                 header=0)

SEED = 37
train, test = model_selection.train_test_split(df, train_size=0.75, random_state=SEED)

dataset = Dataset_2('D:/python/tensorflow2.5/project_ratatouiille/data/ml-1m')
train_2, testRatings, testNegatives = dataset.trainMatrix, dataset.testRatings, dataset.testNegatives

user_input, item_input, labels = get_train_instances(train_2, num_negatives=30)
print(user_input, item_input, labels)
exit()

data = Dataset(col_user='userID', col_item='itemID', col_rating='rating',
                      col_timestamp='timestamp', train=train, test=test, seed=SEED)

user_id = data.users
item_id = data.items
ratings = data.ratings.astype(np.float32)

# print(user_id.dtype)            # int32
# print(item_id.dtype)            # int32
# print(ratings.dtype)            # float32

num_users = data.n_users
num_items = data.n_items
latent_dim = 200
learning_rate = 0.001
topK = 10
evaluation_threads = 1  # mp.cpu_count()
epochs = 10
batch_size = 32
num_negatives = 4

get_model(num_users, num_items, latent_dim)

testRatings = data.test_ratings
testNegatives = data.test_data

print(testRatings)
print(testNegatives)
exit()

if __name__ == '__main__':
    # args = parse_args()
    # num_factors = args.num_factors
    # regs = eval(args.regs)
    # num_negatives = args.num_neg
    # learner = args.learner
    # learning_rate = args.lr
    # epochs = args.epochs
    # batch_size = args.batch_size
    # verbose = args.verbose
    #
    # topK = 10
    # evaluation_threads = 1  # mp.cpu_count()
    # print("GMF arguments: %s" % (args))
    # model_out_file = 'Pretrain/%s_GMF_%d_%d.h5' % (args.dataset, num_factors, time())
    #
    # # Loading data
    # t1 = time()
    # dataset = Dataset(args.path + args.dataset)
    # train, testRatings, testNegatives = dataset.trainMatrix, dataset.testRatings, dataset.testNegatives
    # num_users, num_items = train.shape
    # print("Load data done [%.1f s]. #user=%d, #item=%d, #train=%d, #test=%d"
    #       % (time() - t1, num_users, num_items, train.nnz, len(testRatings)))

    # Build model
    model = get_model(num_users, num_items, latent_dim)
    # model.compile(optimizer=Adagrad(lr=learning_rate), loss='binary_crossentropy')
    # model.compile(optimizer=RMSprop(lr=learning_rate), loss='binary_crossentropy')
    model.compile(optimizer=Adam(lr=learning_rate), loss='binary_crossentropy', metrics=['acc'])
    # model.compile(optimizer=SGD(lr=learning_rate), loss='binary_crossentropy')
    # print(model.summary())

    history = model.fit([user_id, item_id], ratings, epochs=epochs, batch_size=batch_size, verbose=2, shuffle=True)

    (hits, ndcgs) = evaluate_model(model, testRatings, testNegatives, topK, evaluation_threads)
    hr, ndcg, loss = np.array(hits).mean(), np.array(ndcgs).mean(), history.history['loss'][0]
    print('Iteration %d HR = %.4f, NDCG = %.4f, loss = %.4f' % (epochs, hr, ndcg, loss))

    exit()

    # Init performance
    t1 = time()
    (hits, ndcgs) = evaluate_model(model, testRatings, testNegatives, topK, evaluation_threads)
    hr, ndcg = np.array(hits).mean(), np.array(ndcgs).mean()
    # mf_embedding_norm = np.linalg.norm(model.get_layer('user_embedding').get_weights())+np.linalg.norm(model.get_layer('item_embedding').get_weights())
    # p_norm = np.linalg.norm(model.get_layer('prediction').get_weights()[0])
    print('Init: HR = %.4f, NDCG = %.4f\t [%.1f s]' % (hr, ndcg, time() - t1))

    # Train model
    best_hr, best_ndcg, best_iter = hr, ndcg, -1
    for epoch in range(epochs):
        t1 = time()
        # Generate training instances
        user_input, item_input, labels = get_train_instances(train, num_negatives)

        # Training
        hist = model.fit(train,batch_size, nb_epoch=1, verbose=0, shuffle=True)
        t2 = time()

        # Evaluation
        if epoch % verbose == 0:
            (hits, ndcgs) = evaluate_model(model, testRatings, testNegatives, topK, evaluation_threads)
            hr, ndcg, loss = np.array(hits).mean(), np.array(ndcgs).mean(), hist.history['loss'][0]
            print('Iteration %d [%.1f s]: HR = %.4f, NDCG = %.4f, loss = %.4f [%.1f s]'
                  % (epoch, t2 - t1, hr, ndcg, loss, time() - t2))
            if hr > best_hr:
                best_hr, best_ndcg, best_iter = hr, ndcg, epoch
                if args.out > 0:
                    model.save_weights(model_out_file, overwrite=True)

    print("End. Best Iteration %d:  HR = %.4f, NDCG = %.4f. " % (best_iter, best_hr, best_ndcg))
    if args.out > 0:
        print("The best GMF model is saved to %s" % (model_out_file))




