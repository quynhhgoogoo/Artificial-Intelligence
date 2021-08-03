import csv
import random

from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split

# model = Perceptron()
# model = svm.SVC()
# model = KNeighborsClassifier(n_neighbors=1)
model = GaussianNB()

# Read data from csv file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    # Retrieve a list of data, with 4 first values are input and last value is output 
    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row [:4]],
            "label": "Authentic" if row[4] == "0" else "Counterfeit"
        })

# Split the input and output from the dataset
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]

# Seperate data into training and testing groups
# X_training: training input, Y_training: training output
# X_testing: testing input, Y_testing: testing output
X_training, X_testing, Y_training, Y_testing = train_test_split (
    evidence, labels, test_size = 0.4
)

# Train model on training set
model.fit(X_training, Y_training)

# Make predictions on testing set
predictions = model.predict(X_testing)

# Compute how well model performed
correct = (Y_testing == predictions).sum()
incorrect = (Y_testing != predictions).sum()
total = len(predictions)

# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")