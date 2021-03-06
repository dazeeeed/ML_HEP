# -*- coding: utf-8 -*-
from utilities import prepare_set, high_score, save_result, get_Xy

from tree_model import Decision_tree
from svc_model import SVC_classifier
from lr import LR

from datetime import datetime

def test_clf(model, learning_samples, testing_samples, SB_big_ratio, with_PCA):
    X_train, y_train, X_test, y_test = get_Xy(learning_samples, testing_samples, SB_big_ratio)

    clf = model
    clf.fit(X_train, y_train)
    clf.calc_efficiency(X_test, y_test)

    # time, score, params
    return clf.get_params()

if __name__ == "__main__":
    # True to wtedy jest 1:350 sygnal do tla, jak False to 1:2
    SB_big_ratio = True

    # Dla SB_big_ratio True:
    # Max learning = 100 000, testing = 11 000
    #
    # Dla SB_big_ratio False:
    # Max learning = 60 000, testing = 7 000

    learning_samples = 10000
    testing_samples = 5000

    # czy algorytm (oprocz DecisionTree) ma uzyc PCA czy nie
    with_PCA = True

    clfs = [Decision_tree(), SVC_classifier(with_PCA=with_PCA), LR(with_PCA=with_PCA)]

    # TUTAJ USTAW, JAKI MODEL DO SYMULACJI
    model = clfs[1]

    time, score, params = test_clf(model, learning_samples, testing_samples, 
                SB_big_ratio, with_PCA)

    if SB_big_ratio:
        ratio = '1:350'
    else:
        ratio = '1:2'

    if model == clfs[0]:
        model_str = 'decision_tree'
    if model == clfs[1]:
        model_str = 'SVC'
    if model == clfs[2]:
        model_str = 'LogisticRegression'

    text_to_save = f'Time {datetime.now()} \nModel {model_str} \nSB_ratio {ratio} \nPCA {with_PCA} \nTraining_time: {time}s \nEfficiency: {score} \nBest params: {params}\n\n\n'

    print(text_to_save)

    save_result(model_str, text_to_save)