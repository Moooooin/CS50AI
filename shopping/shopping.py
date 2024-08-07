import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = []
    labels = []
    
    # Open & Read CSV into dict
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            cur_user = ([],[])
            keys = list(row.keys())

            for thing in keys[0:-1]:
                cur_user[0].append(thing)
                cur_user[1].append(row[thing])

            # Check length
            if len(cur_user[0]) != 17 or len(cur_user[1]) != 17:
                raise ImportError

            # Values -> Int
            for x in ["Administrative", "Informational", "ProductRelated", 
                        "OperatingSystems", "Browser", "Region", "TrafficType"]:
                index = cur_user[0].index(x)
                try:
                    cur_user[1][index] = int(cur_user[1][index])
                except ValueError:
                    raise ValueError
                
            # Values -> Float
            for x in ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", 
                        "BounceRates", "ExitRates", "PageValues", "SpecialDay"]:
                index = cur_user[0].index(x)
                try:
                    cur_user[1][index] = float(cur_user[1][index])
                except ValueError:
                    raise ValueError

            # Months -> Int 
            months = {
                'Jan' : 0, 'Feb' : 1, 'Mar' : 2, 'Apr' : 3,
                'May' : 4, 'June' : 5, 'Jul' : 6, 'Aug' : 7,
                'Sep' : 8, 'Oct' : 9, 'Nov' : 10, 'Dec' : 11,
            }
            index = cur_user[0].index("Month")
            cur_user[1][index] = months[cur_user[1][index]]

            # Visitor Type -> Int
            index = cur_user[0].index("VisitorType")
            x = cur_user[1][index]
            cur_user[1][index] = 1 if x == 'Returning_Visitor' else 0

            # Weekend -> Int
            index = cur_user[0].index("Weekend")
            x = cur_user[1][index]
            cur_user[1][index] = 1 if x == 'TRUE' else 0

            # Add to lists
            labels.append(1 if row["Revenue"] == 'TRUE' else 0)
            evidence.append(cur_user[1])

    # Return Tuple with Labels + Evidence
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    model = KNeighborsClassifier(n_neighbors=1)

    # Separate Data into Training and Testing set
    holdout = int(TEST_SIZE * len(labels))
    testing = (evidence[:holdout], labels[:holdout])
    training = (evidence[holdout:], labels[holdout:])

    # Train Model on Training set
    model.fit(training[0], training[1])

    # Return trained Model
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Count True and False Positive and Negative Predictions
    pos1 = 0
    pos0 = 0
    neg1 = 0
    neg0 = 0

    for i in range(len(labels)):
        pred = predictions[i]
        label = labels[i]

        if label == 1:
            if pred == label:
                pos1 += 1
            else:
                pos0 += 1

        else:
            if pred == label:
                neg1 += 1
            else:
                neg0 += 1

    return (float(pos1 / (pos0 + pos1)), float(neg1 / (neg0 + neg1)))


if __name__ == "__main__":
    main()
