import csv
import random

from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

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

# Seperate data into training and testing groups
holdout = int(0.4 * len(data))
random.shuffle(data)
testing = data[:holdout]
training = data[holdout:]

# Train model on training set
X_training = [row["evidence"] for row in training]
Y_training = [row["label"] for row in training]
model.fit(X_training, Y_training)

# Make predictions on testing set
X_testing = [row["evidence"] for row in testing]
Y_testing = [row["label"] for row in testing]
predictions = model.predict(X_testing)

# Compute how well model performed
correct = 0
incorrect = 0
total = 0

for actual, predicted in zip(Y_testing, predictions):
    total += 1
    if actual == predicted:
        correct += 1
    else:
        incorrect += 1

# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")