import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import tree
from sklearn import preprocessing


def load_data():
    T1 = []
    T0 = []
    l = 1
    with open("ones.txt", "r") as f:
        for line in f.readlines():
            split_line = [float(x) for x in line.split()]
            if len(split_line) != 10:
                print(l)
                quit()
            l += 1
            T1.append(split_line)
    l = 1
    print("------------")
    with open("zeros.txt", "r") as f:
        for line in f.readlines():
            split_line = [float(x) for x in line.split()]
            if len(split_line) != 10:
                print(l)
                quit()
            l += 1
            T0.append(split_line)

    T1 = np.array(T1)
    T0 = np.array(T0)
    # T1, T0 = T1[:5000, :], T0[:5000, :]
    np.random.shuffle(T0)
    length1 = T1.shape[0]
    T0 = T0[:length1, :]
    T = np.append(T1, T0, axis=0)
    np.random.shuffle(T)
    # print(T[0])
    return T[:, :3], T[:, -1]


def accuracy(y_true, y_predict):
    equals = (y_true == y_predict)
    correct = np.sum(equals)
    total = len(y_true)
    return (correct / total) * 100


def model(model):
    X, Y = load_data()
    X_t = preprocessing.scale(X)
    print("got X, Y")
    clf = None
    if model == "tree":
        clf = DecisionTreeClassifier(max_depth=400)
        clf.fit(X_t, Y)
        tree.export_graphviz(clf, out_file="tree.dot")
    elif model == "svm":
        print("Intializing SVC")
        clf = SVC(max_iter=5000)
        print("Training...")
        clf.fit(X_t, Y)
        print("completed")
    elif model == "linearsvm":
        print("Intializing LinearSVC")
        clf = LinearSVC(max_iter=5000)
        clf.fit(X_t, Y)
    return clf,  X.mean(axis=0), X.std(axis=0)