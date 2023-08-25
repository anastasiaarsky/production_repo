from src.features import build_ml_features
from src.models.ml_model.train_ml_model import calculate_metrics

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


def main():
    # Get the training, validation, and testing sets
    X_train_full_vec, y_train_full, X_test_vec, y_test = build_ml_features.main(train=False)

    # Random Forest Testing Results on Word Level TF-IDF Vectors
    # (using the entire training set and the testing set)
    classifier = RandomForestClassifier()

    # Fit the training dataset on the classifier
    classifier.fit(X_train_full_vec, y_train_full)

    # Predict the labels on validation dataset
    y_pred = classifier.predict(X_test_vec)

    # Print metrics results
    calculate_metrics(y_test, y_pred)

    # Print classification report & confusion matrix
    print(classification_report(y_test, y_pred))
    print(pd.DataFrame(confusion_matrix(y_test, y_pred)))


if __name__ == "__main__":
    main()
