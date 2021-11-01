# dataset.py
import scipy.sparse as sp
import numpy as np


class Dataset(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.trainMatrix = self.load_rating_file_as_matrix(path + ".train.rating")
        self.testLabels = self.load_label_file_as_list(path + ".test.label")
        self.testPredictions = self.load_predict_file(path + ".test.preds")
        assert len(self.testLabels) == len(self.testPredictions)

        self.num_users, self.num_items = self.trainMatrix.shape

    def load_label_file_as_list(self, filename):
        labelList = []
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split(',')
                user, item = int(arr[0]) - 1, [int(n) - 1 for n in arr[1:]]
                labelList.append([user, item])
                line = f.readline()
        return labelList

    def load_predict_file(self, filename):
        predictList = []
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split()
                negatives = []
                for x in arr[1:]:
                    negatives.append(int(x) - 1)
                predictList.append(negatives)
                line = f.readline()
        return predictList

    def load_rating_file_as_matrix(self, filename):
        '''
        Read .rating file and Return dok matrix.
        The first line of .rating file is: num_users\t num_items
        '''
        # Get number of users and items
        num_users, num_items = 0, 0
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                u, i = int(arr[0]) - 1, int(arr[1]) - 1
                num_users = max(num_users, u)
                num_items = max(num_items, i)
                line = f.readline()
        # Construct matrix
        mat = sp.dok_matrix((num_users + 1, num_items + 1), dtype=np.float32)
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                user, item, rating = int(arr[0]) - 1, int(arr[1]) - 1, float(arr[2])
                if (rating > 0):
                    mat[user, item] = 1.0
                line = f.readline()
        return mat
