#!/usr/bin/env python
# coding: utf-8
import numpy as np
import sklearn
# from sklearn.model_selection import train_test_split
from numpy import ndarray
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, make_scorer
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.model_selection import (
    LeaveOneOut,
    LeavePOut,
    RepeatedStratifiedKFold,
    StratifiedShuffleSplit,
)
import utils


def train_test_split(X: np.ndarray, y: np.ndarray, test_size: float, random_state: int)\
        -> [np.array, np.array, np.array, np.array]:
    """Splits the given dataset into random train and test subsets.
     The `test_size` defines the proportion of the test set."""
    assert(len(X) == len(y))
    assert(test_size >= 0)
    assert(test_size <= 1)

    np.random.seed(random_state)
    nb_test_samples = round(len(X) * test_size)
    test_indices = np.zeros(len(X), dtype=bool)
    test_indices[:nb_test_samples] = True
    np.random.shuffle(test_indices)
    train_indices = ~test_indices

    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]

def train_test_split2(X: np.ndarray, y: np.ndarray, test_size: float, random_state: int)\
        -> [np.array, np.array, np.array, np.array]:
    assert (len(X) == len(y))
    assert (test_size >= 0)
    assert (test_size <= 1)
    # boolean Array mit länge X
    test_indices = np.random.choice([True, False], size=len(X), p=[test_size, 1 - test_size])
    train_indices = ~test_indices
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]

# X_train= X\X_i X_test=X_i (X=X_1,...X_k)
def acc_kfold_cross_val(clf: sklearn.base.BaseEstimator, cv: sklearn.model_selection._split._BaseKFold,
                        X: np.ndarray, y: np.ndarray) -> (float, float):
    """Runs cross validation for the given classifier and cross validation method and
     returns the mean train and test accuracy."""
    'sklearn.base.BaseEstimator:'
    '''https://scikit-learn.org/stable/modules/generated/sklearn.base.BaseEstimator.html'''

    'make_scorer:'
    '''https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html'''
    # make_scorer makes a scorer from a score function
    # accuracy_score computes accuracy between y_true and y_pred

    '''https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html'''
    # clf=estimator object to use to fit the data
    #X=Data to fit (array, list), y= target variable, try to predict
    # cv = cross validation strategy
    # scoring = strategy to evaluate the performance of the cross validated model
    # make_scorer makes a scorer from a score function

    scores = cross_validate(clf, X, y, cv=cv, scoring=make_scorer(accuracy_score), return_train_score = True)
    # train score und test score heißen die Ausgaben, mit scores können diese aufgerufen werden
    mean_acc_train = scores['train_score'].mean()
    mean_acc_test = scores['test_score'].mean()
    return mean_acc_train, mean_acc_test





def main():
    # Load data
    X, y = utils.generate_dataset()

    # Run train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # Plot
    utils.plot_two_class_dataset(X_test, X_train, y_test, y_train)

    # Train
    clf = DecisionTreeClassifier(random_state=0)
    acc_test, acc_train = utils.measure_accuracy(clf, X_test, X_train, y_test, y_train)
    print(f"Accuracy Train:  {acc_train * 100: >3.2f} %")
    print(f"Accuracy Test :  {acc_test * 100: >3.2f} %")

    # Create cross-validation methods
    cvs = [
        (StratifiedKFold(n_splits=10, shuffle=True, random_state=0), "KFold"),
        (RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=0), "Repeated KFold"),
        (LeaveOneOut(), "Leave One Out"),
        (LeavePOut(p=5), "Leave P Out (p = 5)"),
        (StratifiedShuffleSplit(n_splits=10, test_size=0.33, random_state=0), "Shuffle Split"),
    ]

    # Print accuracy for each cross-validation method
    print("-" * 100)
    for cv, name in cvs:
        # Run cross validation
        mean_acc_train, mean_acc_test = acc_kfold_cross_val(clf, cv, X, y)

        # Print scores
        print(f"Train Accuracy mean for {name: <21}: {mean_acc_train * 100:3.2f} %")
        print(f" Test Accuracy mean for {name: <21}: {mean_acc_test * 100:3.2f} %")
        print("-" * 100)
        # Gap zwischen Trainings und Testdaten relativ groß -> Overfitting; zu sehr an Testdaten gewöhnt

if __name__ == '__main__':
    main()
