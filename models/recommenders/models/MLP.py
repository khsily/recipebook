# MLP.py
import numpy as np

import tensorflow as tf
from keras import backend as K
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.regularizers import l2
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Lambda, Activation
from tensorflow.keras.layers import Embedding, Input, Dense, Reshape, concatenate, add, Flatten, Dropout
from tensorflow.keras.constraints import max_norm
from tensorflow.keras.optimizers import Adagrad, Adam, SGD, RMSprop
from evaluate import evaluate_model
from dataset import Dataset
from time import time
import sys
import argparse
import multiprocessing as mp


#################### Arguments ####################
def parse_args():
    parser = argparse.ArgumentParser(description="Run MLP.")
    parser.add_argument('--path', nargs='?', default='D:\python\\tensorflow2.5\project_ratatouiille\data/',
                        help='Input data path.')
    parser.add_argument('--dataset', nargs='?', default='ml-1m',
                        help='Choose a dataset.')
    parser.add_argument('--epochs', type=int, default=1,
                        help='Number of epochs.')
    parser.add_argument('--batch_size', type=int, default=256,
                        help='Batch size.')
    parser.add_argument('--layers', nargs='?', default='[64,32,16,8]',
                        help="Size of each layer. Note that the first layer is the concatenation of user and item embeddings. So layers[0]/2 is the embedding size.")
    parser.add_argument('--reg_layers', nargs='?', default='[0,0,0,0]',
                        help="Regularization for each layer")
    parser.add_argument('--num_neg', type=int, default=4,
                        help='Number of negative instances to pair with a positive instance.')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='Learning rate.')
    parser.add_argument('--learner', nargs='?', default='adam',
                        help='Specify an optimizer: adagrad, adam, rmsprop, sgd')
    parser.add_argument('--verbose', type=int, default=1,
                        help='Show performance per X iterations')
    parser.add_argument('--out', type=int, default=1,
                        help='Whether to save the trained model.')
    return parser.parse_args()


def get_model(num_users, num_items, layers=[20, 10], reg_layers=[0, 0]):
    assert len(layers) == len(reg_layers)
    num_layer = len(layers)  # Number of layers in the MLP
    # Input variables
    user_input = Input(shape=(1,), dtype='int32', name='user_input')
    item_input = Input(shape=(1,), dtype='int32', name='item_input')

    MLP_Embedding_User = Embedding(input_dim=num_users, output_dim=layers[0] // 2, name='user_embedding',
                                   embeddings_initializer=glorot_uniform,
                                   embeddings_regularizer=tf.keras.regularizers.l2(l2=reg_layers[0]), input_length=1)
    MLP_Embedding_Item = Embedding(input_dim=num_items, output_dim=layers[0] // 2, name='item_embedding',
                                   embeddings_initializer=glorot_uniform,
                                   embeddings_regularizer=tf.keras.regularizers.l2(l2=reg_layers[0]), input_length=1)

    # Crucial to flatten an embedding vector!
    user_latent = Flatten()(MLP_Embedding_User(user_input))
    item_latent = Flatten()(MLP_Embedding_Item(item_input))

    # The 0-th layer is the concatenation of embedding layers
    vector = concatenate([user_latent, item_latent])

    # MLP layers
    for idx in range(1, num_layer):
        layer = Dense(layers[idx], kernel_regularizer=tf.keras.regularizers.l2(l2=reg_layers[idx]),
                      activation='relu', name='layer%d' % idx)
        vector = layer(vector)

    # Final prediction layer
    prediction = Dense(1, activation='sigmoid', name='prediction')(vector)

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
            while (u, j) in train:
                j = np.random.randint(num_items)
            user_input.append(u)
            item_input.append(j)
            labels.append(0)
    return user_input, item_input, labels


if __name__ == '__main__':
    args = parse_args()
    path = args.path
    dataset = args.dataset
    layers = eval(args.layers)
    reg_layers = eval(args.reg_layers)
    num_negatives = args.num_neg
    learner = args.learner
    learning_rate = args.lr
    batch_size = args.batch_size
    epochs = args.epochs
    verbose = args.verbose

    topK = 10
    evaluation_threads = 1  # mp.cpu_count()
    print("MLP arguments: %s " % (args))
    model_out_file = 'D:\python\\tensorflow2.5\project_ratatouiille\model\Pretrain/%s_MLP_%s_%d.h5' \
                     % (args.dataset, args.layers, time())

    # Loading data
    t1 = time()
    data = Dataset(args.path + args.dataset)
    train, testRatings, testNegatives = data.trainMatrix, data.testRatings, data.testNegatives
    num_users, num_items = train.shape
    print("Load data done [%.1f s]. #user=%d, #item=%d, #train=%d, #test=%d"
          % (time() - t1, num_users, num_items, train.nnz, len(testRatings)))

    # Build model
    model = get_model(num_users, num_items, layers, reg_layers)

    # model.compile(optimizer=Adagrad(learning_rate=learning_rate), loss='binary_crossentropy')
    # model.compile(optimizer=RMSprop(learning_rate=learning_rate), loss='binary_crossentropy')
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='binary_crossentropy')
    # model.compile(optimizer=SGD(learning_rate=learning_rate), loss='binary_crossentropy')

    # Check Init performance
    t1 = time()
    (hits, ndcgs) = evaluate_model(model, testRatings, testNegatives, topK, evaluation_threads)
    hr, ndcg = np.array(hits).mean(), np.array(ndcgs).mean()
    print('Init: HR = %.4f, NDCG = %.4f [%.1f]' % (hr, ndcg, time() - t1))

    # Train model
    best_hr, best_ndcg, best_iter = hr, ndcg, -1
    for epoch in range(epochs):
        t1 = time()
        # Generate training instances
        user_input, item_input, labels = get_train_instances(train, num_negatives)

        checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=model_out_file,
                                                        verbose=1,
                                                        save_weights_only=True,
                                                        save_best_only=True,
                                                        save_freq=epoch)
        # Training
        hist = model.fit([np.array(user_input), np.array(item_input)],  # input
                         np.array(labels),  # labels
                         batch_size=batch_size, epochs=1, verbose=0, shuffle=True,
                         callbacks=[checkpoint])
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
                    model.save_weights(model_out_file.format(epoch=0), overwrite=True)

    print("End. Best Iteration %d:  HR = %.4f, NDCG = %.4f. " % (best_iter, best_hr, best_ndcg))
    if args.out > 0:
        print("The best MLP model is saved to %s" % (model_out_file))

