#!/usr/bin/env python
# coding: utf-8
# ## Referenzen
#  [1] C. Cortes and V. Vapnik. „Support-Vector Networks“. In: Machine Learning 20.3 (1995), pp. 273–297
from sklearn import svm
from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import utils
# SVM with different kernels


sns.set(
    context="notebook",
    style="whitegrid",
    rc={"figure.dpi": 120, "scatter.edgecolors": "k"},
)


def plot_data(X, y):
    """Plots the data and label assignment as a scatter plot."""
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired, edgecolors='k', zorder=10)
    # no ticks
    plt.xticks([])
    plt.yticks([])
    # all data is shown
    plt.axis("tight")
    plt.show()


def fit_linear_svm(X, y):
    """Fits a svm with a linear kernel and no regularization to the data."""
    clf = svm.SVC(C=1e10, kernel='linear', max_iter=10000)
    clf.fit(X, y)
    return clf


def fit_rbf_svm(X, y):
    """Fits a svm with a rbf kernel and no regularization to the data."""
    # auto = # of features
    clf = svm.SVC(C=1e10, kernel='rbf', gamma='auto')
    clf.fit(X, y)
    return clf


def plot_svm_C(X, y):
    """Plot the decision boundaries and support vectors for regularization constants:
    C=[2^-6, 2^-3, 1, 2^3, 2^6, 2^12]."""
    C =[2e-6, 2e-3, 1, 2e3, 2e6, 2e12]
    for ci in C:
        clf = svm.SVC(C=ci, kernel='rbf', gamma='auto', max_iter=10000)
        clf.fit(X, y)
        utils.plot_support_vectors(X, y, clf, title=f'C={ci}')



def main():
    # Make experiments reproducible
    np.random.seed(0)

    X_lin, y_lin = datasets.make_blobs(n_samples=40, centers=2, random_state=6)

    plot_data(X_lin, y_lin)

    # Create an SVC object with a linear kernel (and no regularization)
    # Fit the hyperplane to the data
    clf = fit_linear_svm(X_lin, y_lin)

    # Plot data with hyperplane and support vectors
    utils.plot_support_vectors(X_lin, y_lin, clf)

    # Create circles dataset
    X_circ, y_circ = datasets.make_circles(
        n_samples=50, noise=0.2, random_state=6, factor=0.01
    )

    # Plot
    plot_data(X_circ, y_circ)

    # Create an SVC object with the linear kernel parameter
    clf = fit_linear_svm(X_circ, y_circ)

    # Plot data with hyperplane and support vectors
    utils.plot_support_vectors(X_circ, y_circ, clf)

    # Create an SVC object with the rbf kernel parameter
    clf = fit_rbf_svm(X_circ, y_circ)

    # Plot data with hyperplane and support vectors
    utils.plot_support_vectors(X_circ, y_circ, clf)

    # Generate the two moons dataset
    X_moons, y_moons = datasets.make_moons(200, noise=0.4, random_state=6)

    # Plot the data
    plot_data(X_moons, y_moons)
    plot_svm_C(X_moons, y_moons)


if __name__ == '__main__':
    main()
