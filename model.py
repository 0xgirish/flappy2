import numpy as np

from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import preprocessing

from NeuralModel import Neural
from settings import SVM_DATA_ONES, SVM_DATA_ZEROS, POPULATION


def get_data_from_file(filename):
    destination = []
    with open(filename, "r") as f:
        for line in f.readlines():
            split_line = [float(x) for x in line.split()]
            destination.apppend(split_line)

    return np.array(destination)


def load_data():

    ones = get_data_from_file(SVM_DATA_ONES)
    zeros = get_data_from_file(SVM_DATA_ZEROS)

    training_data = np.append(ones, zeros, axis=0)

    return training_data[:, :-1], training_data[:, -1]


def get_model(name="gan"):
    if name.upper() == "GAN":
        neural_list = []
        for _ in range(POPULATION):
            neural_list.append(Neural())

        return neural_list
    elif name.upper() == "SVM":
        X, Y = load_data()
        X_t = preprocessing.scale(X)
        mean = X.mean(axis=0)
        std = X.std(axis=0)
        clf = SVC()
        clf.fit(X_t, Y)
        return clf, mean, std
    elif name.upper() == "LINEARSVM":
        X, Y = load_data()
        X_t = preprocessing.scale(X)
        mean = X.mean(axis=0)
        std = X.std(axis=0)
        clf = LinearSVC()
        clf.fit(X_t, Y)
        return clf, mean, std
    else:
        print("Wrong model")
        quit()