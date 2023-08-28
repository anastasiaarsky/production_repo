from src.features import build_ml_features

import argparse
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix


# Function to print metrics results
def calculate_metrics(y_true, y_pred):
    print("\tTest accuracy: {:.3f}".format(accuracy_score(y_true, y_pred) * 100))
    print("\tF1 Score: {:.3f}".format(f1_score(y_true, y_pred, average='macro') * 100))
    print("\tRecall: {:.3f}".format(recall_score(y_true, y_pred, average='macro') * 100))
    print("\tPrecision: {:.3f}".format(precision_score(y_true, y_pred, average='macro') * 100))


# Function to print a custom confusion matrix with added labels
def print_custom_confusion_matrix(y_true, y_pred):
    labels = ['True Negative', 'Predicted Positive', 'Actual Negative', 'Actual Positive']
    cm = confusion_matrix(y_true, y_pred)

    print('\tConfusion Matrix:')
    print("\t{:20} {:^20} {:^20}".format("", labels[0], labels[1]))
    print("\t{:20} {:^20} {:^20}".format(labels[2], cm[0, 0], cm[0, 1]))
    print("\t{:20} {:^20} {:^20}".format(labels[3], cm[1, 0], cm[1, 1]))


def main(train=True):
    # Step 1: Get training flag (if applicable)
    parser = argparse.ArgumentParser(description="Train a model")
    parser.add_argument('-t', '--train', action='store_true', help='Flag to indicate training')
    args = parser.parse_args()

    # Step 2: Get the training, validation, and testing sets
    X_train_vec, y_train, X_val_vec, y_val, X_test_vec, y_test = build_ml_features.main()

    # Step 3: Train the RF model or load the pretrained RF model
    if args.train:
        print('\nStarting training of the Random Forest model...')

        # Step 3: Create a default Random Forest Classifier since RandomizedSearchCV did not improve results
        rf = RandomForestClassifier()

        # Step 3: Fit the RF Classifier on the training dataset
        rf.fit(X_train_vec, y_train)

        # Step 4: Save the Random Forest model
        joblib.dump(rf, 'models/random_forest_model.joblib')

        # Step 5: Evaluate on the validation dataset
        y_pred = rf.predict(X_val_vec)

        # Step 6: Print metrics results
        print("Evaluation Results on the Validation Set: ")
        calculate_metrics(y_val, y_pred)

        print('Model training completed')

    else:
        rf = joblib.load('models/random_forest_model.joblib')

    print('\nStarting model prediction...')

    # Step 4: Predict on the testing dataset
    y_pred = rf.predict(X_test_vec)

    # Step 5: Print metrics results
    print("Random Forest Prediction Results on the Testing Set:")
    calculate_metrics(y_test, y_pred)

    # Step 6: Print confusion matrix
    print_custom_confusion_matrix(y_test, y_pred)

    print('Model prediction completed')


if __name__ == "__main__":
    main()
