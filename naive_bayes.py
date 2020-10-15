import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import corona_confirmed_for_supervised, corona_recovered_for_supervised, corona_deaths_for_supervised

def naive_bayes_algorithm(data_frame, label):
    cols = list(data_frame.columns)
    cols.remove('Continent')

    X = data_frame[cols].copy()
    y = data_frame['Continent'].copy()

    def split_test_train(X, y, test_size):
        try:
            return train_test_split(X, y, test_size=test_size, random_state=0)
        except:
           print('Something got wrong - split_test_train')

    def create_naive_bayes_classifier(X, y):
        try:
            model = GaussianNB()
            model.fit(X, y)
            return model
        except:
            print('Something got wrong - create_naive_bayes_classifier')

    accuracy = []
    for ratio in np.arange(0.1, 0.5, 0.1):
        X_train, X_test, y_train, y_test = split_test_train(X, y, test_size = ratio)
        model = create_naive_bayes_classifier(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy.append(accuracy_score(y_test, y_pred))

    best_accuracy = 0
    x = 0
    split = None
    for i in accuracy:
        x += 1
        if i > best_accuracy:
            best_accuracy = i
            split = "0." + str(x)
    print('The best accuracy is: ' + str(best_accuracy) +'\nThe size of the test team is: ' + str(split))

    ratios = np.arange(0.1, 0.5, 0.1)
    plt.grid(True)
    plt.plot(ratios, accuracy, 'r--')
    plt.xlabel('Size of Test Set')
    plt.ylabel('Accuracy')
    plt.title('Accuracy over Different Sizes of Train Set', fontsize=15)
    plt.show()

    if label == 'Confusion matrix for Confirmed data frame':
        X_train, X_test, y_train, y_test = split_test_train(X, y, test_size=0.2)
        model = create_naive_bayes_classifier(X_train, y_train)
        y_pred = model.predict(X_test)
        confusion_matrix(y_test, y_pred)
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True)
        plt.title(label)
        plt.show()

    else:
        X_train, X_test, y_train, y_test = split_test_train(X, y, test_size=0.4)
        model = create_naive_bayes_classifier(X_train, y_train)
        y_pred = model.predict(X_test)
        confusion_matrix(y_test, y_pred)
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True)
        plt.title(label)
        plt.show()

naive_bayes_algorithm(corona_confirmed_for_supervised, 'Confusion matrix for Confirmed data frame')
naive_bayes_algorithm(corona_recovered_for_supervised, 'Confusion matrix for Recovered data frame')
naive_bayes_algorithm(corona_deaths_for_supervised, 'Confusion matrix for Deaths data frame')